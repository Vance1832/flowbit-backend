from rest_framework import serializers
from .models import SettlementBatch, SettlementItem, SettlementItemSource


class SettlementItemSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettlementItemSource
        fields = "__all__"


class SettlementItemSerializer(serializers.ModelSerializer):
    sources = SettlementItemSourceSerializer(many=True, read_only=True)

    class Meta:
        model = SettlementItem
        fields = "__all__"


class SettlementBatchSerializer(serializers.ModelSerializer):
    items = SettlementItemSerializer(many=True, read_only=True)

    class Meta:
        model = SettlementBatch
        fields = "__all__"