from django.contrib import admin
from .models import CompanyWallet, CompanyWalletTransaction, CompanyCashoutRequest


@admin.register(CompanyWallet)
class CompanyWalletAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "balance", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(CompanyWalletTransaction)
class CompanyWalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_wallet",
        "transaction_type",
        "amount",
        "balance_before",
        "balance_after",
        "created_by",
        "created_at",
    )
    list_filter = ("transaction_type", "created_at")
    search_fields = ("company_wallet__name", "description")
    readonly_fields = ("created_at",)


@admin.register(CompanyCashoutRequest)
class CompanyCashoutRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_wallet",
        "requested_by",
        "approved_by",
        "amount",
        "status",
        "approved_at",
        "paid_at",
        "created_at",
    )
    list_filter = ("status", "created_at", "approved_at", "paid_at")
    search_fields = ("requested_by__name", "approved_by__name", "reason", "admin_note")
    readonly_fields = ("created_at", "updated_at")