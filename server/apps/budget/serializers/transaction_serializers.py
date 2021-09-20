from rest_framework import serializers

from apps.budget.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('category', 'amount', 'date')

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


class TransactionListSerializer(serializers.ModelSerializer):
    category_type = serializers.ReadOnlyField(source='category.category_type')

    class Meta:
        model = Transaction
        fields = ('id', 'category_type', 'category', 'amount', 'date')


class TransactionGlobalSerializer(serializers.ModelSerializer):
    category_type = serializers.ReadOnlyField(source='category__category_type')
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = ('total_amount', 'category_type')
