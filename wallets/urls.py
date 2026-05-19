from django.urls import path
from .views import (
    MyWalletView,
    MyWalletTransactionListView,
    DepositRequestListCreateView,
    WithdrawalRequestListCreateView,
)


urlpatterns = [
    path("me/", MyWalletView.as_view(), name="my-wallet"),
    path("transactions/", MyWalletTransactionListView.as_view(), name="wallet-transactions"),
    path("deposits/", DepositRequestListCreateView.as_view(), name="deposit-requests"),
    path("withdrawals/", WithdrawalRequestListCreateView.as_view(), name="withdrawal-requests"),
]