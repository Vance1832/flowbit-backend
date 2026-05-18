from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import DepositRequest, UserWallet, WalletTransaction, WithdrawalRequest


@transaction.atomic
def assign_deposit_request(deposit_request: DepositRequest, staff_user):
    deposit_request = DepositRequest.objects.select_for_update().get(id=deposit_request.id)

    if deposit_request.status != DepositRequest.Status.PENDING:
        raise ValueError("Only pending deposit requests can be assigned.")

    deposit_request.status = DepositRequest.Status.IN_REVIEW
    deposit_request.assigned_to = staff_user
    deposit_request.assigned_at = timezone.now()
    deposit_request.save(update_fields=["status", "assigned_to", "assigned_at", "updated_at"])

    return deposit_request


@transaction.atomic
def approve_deposit_request(deposit_request: DepositRequest, staff_user, staff_note=None):
    deposit_request = DepositRequest.objects.select_for_update().get(id=deposit_request.id)

    if deposit_request.status not in [
        DepositRequest.Status.PENDING,
        DepositRequest.Status.IN_REVIEW,
    ]:
        raise ValueError("Only pending or in-review deposits can be approved.")

    wallet = UserWallet.objects.select_for_update().get(id=deposit_request.wallet_id)

    balance_before = wallet.balance
    wallet.balance += deposit_request.amount
    wallet.save(update_fields=["balance", "updated_at"])

    wallet_transaction = WalletTransaction.objects.create(
        wallet=wallet,
        user=deposit_request.user,
        transaction_type=WalletTransaction.TransactionType.DEPOSIT,
        amount=deposit_request.amount,
        balance_before=balance_before,
        balance_after=wallet.balance,
        reference_table="deposit_requests",
        reference_id=deposit_request.id,
        description="Deposit approved",
        created_by=staff_user,
    )

    deposit_request.status = DepositRequest.Status.APPROVED
    deposit_request.reviewed_by = staff_user
    deposit_request.reviewed_at = timezone.now()

    if staff_note:
        deposit_request.staff_note = staff_note

    deposit_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "staff_note",
            "updated_at",
        ]
    )

    return deposit_request, wallet_transaction


@transaction.atomic
def reject_deposit_request(deposit_request: DepositRequest, staff_user, staff_note=None):
    deposit_request = DepositRequest.objects.select_for_update().get(id=deposit_request.id)

    if deposit_request.status not in [
        DepositRequest.Status.PENDING,
        DepositRequest.Status.IN_REVIEW,
    ]:
        raise ValueError("Only pending or in-review deposits can be rejected.")

    deposit_request.status = DepositRequest.Status.REJECTED
    deposit_request.reviewed_by = staff_user
    deposit_request.reviewed_at = timezone.now()

    if staff_note:
        deposit_request.staff_note = staff_note

    deposit_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "staff_note",
            "updated_at",
        ]
    )

    return deposit_request