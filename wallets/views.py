from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    UserWallet,
    WalletTransaction,
    DepositRequest,
    WithdrawalRequest,
)
from .serializers import (
    UserWalletSerializer,
    WalletTransactionSerializer,
    DepositRequestSerializer,
    WithdrawalRequestSerializer,
)


class MyWalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, _ = UserWallet.objects.get_or_create(user=request.user)
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data)


class MyWalletTransactionListView(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletTransaction.objects.filter(user=self.request.user).order_by("-created_at")


class DepositRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = DepositRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DepositRequest.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        wallet, _ = UserWallet.objects.get_or_create(user=self.request.user)
        serializer.save(user=self.request.user, wallet=wallet)


class WithdrawalRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        wallet, _ = UserWallet.objects.get_or_create(user=self.request.user)
        serializer.save(user=self.request.user, wallet=wallet)