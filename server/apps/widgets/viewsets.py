from django.db.models import F, DateTimeField, ExpressionWrapper, Sum, FilteredRelation, Q
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from apps.widgets.serializers import (
    WidgetCreateSerializer,
    WidgetListSerializer
)
from apps.widgets.models import Widget
from apps.users.permissions import OwnerOnly


class WidgetViewSet(GenericViewSet, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated, OwnerOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Widget.objects.all()
        if self.action == 'list':
            expr_date = ExpressionWrapper(F('validity') + F('created_at'), output_field=DateTimeField())
            date_lte_expr = F('created_at') + F('validity')
            date_gte_expr = F('created_at')
            filter_expr = Q(category__transactions__owner=self.request.user,
                            category__transactions__date__gte=date_gte_expr,
                            category__transactions__date__lte=date_lte_expr)
            queryset = queryset.filter(owner=self.request.user). \
                annotate(date_end=expr_date).select_related('category'). \
                prefetch_related('category__transactions'). \
                annotate(filtered_transactions=FilteredRelation('category__transactions', condition=filter_expr)). \
                annotate(amount_spent=Coalesce(Sum('filtered_transactions__amount'), .0))
        return queryset

    def get_serializer_class(self):
        serializer = WidgetCreateSerializer
        if self.action == 'list':
            serializer = WidgetListSerializer
        return serializer
