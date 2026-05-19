from settlements.models import SettlementItem
from audit.models import AuditLog
from audit.services import create_audit_log


def get_user_visible_results(user):
    """
    Normal user result page:
    - show result date
    - show result number
    - only show matched status if user's settlement item is paid
    """

    from .models import ResultPeriod

    result_periods = (
        ResultPeriod.objects
        .filter(
            is_visible_to_users=True,
            result_number__isnull=False,
        )
        .exclude(result_number="")
        .order_by("-result_date")
    )

    results = []

    for period in result_periods:
        data = {
            "result_date": period.result_date,
            "result_number": period.result_number,
        }

        matched_paid = SettlementItem.objects.filter(
            settlement_batch__result_period=period,
            user=user,
            status=SettlementItem.Status.PAID,
        ).exists()

        if matched_paid:
            data["status"] = "Matched - Confirmed and Paid Out"

        results.append(data)

    return results

from django.db import transaction
from django.utils import timezone

from settlements.services import create_settlement_preview


@transaction.atomic
def close_result_period(result_period, admin_user):
    result_period = result_period.__class__.objects.select_for_update().get(id=result_period.id)
    previous_status = result_period.status

    if result_period.status not in [
        result_period.Status.OPEN,
        result_period.Status.CLOSED,
    ]:
        raise ValueError("Only open or closed result periods can be closed.")

    result_period.status = result_period.Status.CLOSED
    result_period.save(update_fields=["status", "updated_at"])

    ledgers = result_period.ledgers.select_for_update().filter(status="open")

    for ledger in ledgers:
        ledger.status = "closed"
        ledger.manually_closed_by = admin_user
        ledger.manually_closed_at = timezone.now()
        ledger.save(update_fields=["status", "manually_closed_by", "manually_closed_at", "updated_at"])

    create_audit_log(
        actor_user=admin_user,
        action=AuditLog.ActionType.CLOSE,
        target_table="result_periods",
        target_id=result_period.id,
        old_values={"status": previous_status},
        new_values={"status": result_period.status},
        reason="Result period closed.",
    )

    return result_period


@transaction.atomic
def enter_result_and_preview_settlement(result_period, result_number, admin_user):
    result_period = result_period.__class__.objects.select_for_update().get(id=result_period.id)
    previous_status = result_period.status

    if result_period.status not in [
        result_period.Status.CLOSED,
        result_period.Status.OPEN,
    ]:
        raise ValueError("Result can only be entered for open or closed result periods.")

    if result_period.status == result_period.Status.OPEN:
        close_result_period(result_period, admin_user)

    batch = create_settlement_preview(
        result_period=result_period,
        result_number=result_number,
        admin_user=admin_user,
    )

    create_audit_log(
        actor_user=admin_user,
        action=AuditLog.ActionType.RESULT_ENTRY,
        target_table="result_periods",
        target_id=result_period.id,
        old_values={"status": previous_status},
        new_values={
            "status": result_period.Status.SETTLEMENT_PREVIEWED,
            "result_number": batch.result_number,
            "settlement_batch_id": batch.id,
        },
        reason="Result entered and settlement preview created.",
    )

    return batch
