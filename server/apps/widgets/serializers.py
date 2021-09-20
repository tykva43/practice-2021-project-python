from rest_framework import serializers

from apps.widgets.models import Widget


class WidgetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Widget
        fields = ('category', 'money_limit', 'validity', 'criterion', 'color', 'created_at')


class WidgetListSerializer(serializers.ModelSerializer):
    amount_spent = serializers.ReadOnlyField()
    date_end = serializers.ReadOnlyField()

    class Meta:
        model = Widget
        fields = ('id', 'category', 'money_limit', 'validity', 'criterion',
                  'color', 'created_at', 'amount_spent', 'date_end')
