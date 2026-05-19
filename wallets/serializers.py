from rest_framework import serializers
from .models import (
    UserWallet,
    WalletTransaction,
    DepositRequest,
    WithdrawalRequest,
)


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ("id", "balance", "locked_balance", "created_at", "updated_at")
        read_only_fields = fields


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = (
            "id",
            "transaction_type",
            "amount",
            "balance_before",
            "balance_after",
            "reference_table",
            "reference_id",
            "description",
            "created_at",
        )
        read_only_fields = fields


class DepositRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositRequest
        fields = (
            "id",
            "amount",
            "payment_method",
            "sender_account_name",
            "transaction_reference",
            "proof_image_url",
            "user_note",
            "staff_note",
            "status",
            "assigned_to",
            "assigned_at",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "staff_note",
            "status",
            "assigned_to",
            "assigned_at",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )

    def validate_amount(self, value):
        if value < 1000:
            raise serializers.ValidationError("Minimum deposit amount is 1000.")
        return value


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = (
            "id",
            "amount",
            "payment_account_name",
            "payment_account_number",
            "payment_method",
            "user_note",
            "staff_note",
            "status",
            "reviewed_by",
            "reviewed_at",
            "paid_by",
            "paid_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "staff_note",
            "status",
            "reviewed_by",
            "reviewed_at",
            "paid_by",
            "paid_at",
            "created_at",
            "updated_at",
        )

    def validate_amount(self, value):
        if value < 10000:
            raise serializers.ValidationError("Minimum withdrawal amount is 10000.")
        return value
    