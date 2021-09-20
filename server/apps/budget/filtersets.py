from django_filters import rest_framework as filters

from apps.budget.models import Transaction


class TransactionFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date']
