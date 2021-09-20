from rest_framework import serializers

from apps.budget.models import TransactionCategory


class TransactionCategoryCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return TransactionCategory.objects.create(**validated_data)

    class Meta:
        model = TransactionCategory
        fields = ('category_type', 'name')


class TransactionCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionCategory
        fields = ('id', 'category_type', 'name')


class TransactionCategorySumsSerializer(serializers.ModelSerializer):
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = TransactionCategory
        fields = ('id', 'category_type', 'name', 'total_amount')
