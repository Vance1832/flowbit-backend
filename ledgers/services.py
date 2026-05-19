from settlements.models import SettlementItem


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