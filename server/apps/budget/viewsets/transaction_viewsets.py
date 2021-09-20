from django.db.models import Sum
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.budget.models import Transaction
from apps.budget.serializers import (
    TransactionSerializer,
    TransactionListSerializer,
    TransactionGlobalSerializer
)
from apps.budget.paginator import TransactionSetPagination
from apps.budget.filtersets import TransactionFilter
from apps.users.permissions import OwnerOnly


class TransactionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                         mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated, OwnerOnly]
    pagination_class = TransactionSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self, month=None, year=None):
        queryset = Transaction.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(owner=self.request.user).select_related('category')
        if self.action == 'global_data':
            queryset = queryset.filter(owner=self.request.user).select_related('category').\
                values('category__category_type').annotate(total_amount=Sum(Coalesce('amount', .0)))
        return queryset

    def get_serializer_class(self):
        serializer = TransactionSerializer
        if self.action == 'list':
            serializer = TransactionListSerializer
        if self.action == 'global_data':
            serializer = TransactionGlobalSerializer
        return serializer

    def get_category_data(self, queryset, category_type):
        if queryset.filter(category__category_type=category_type).exists():
            obj = queryset.get(category__category_type=category_type)
        else:
            obj = {'category__category_type': category_type, 'total_amount': .0}
        return obj

    @action(detail=False, methods=['get'])
    def global_data(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        global_list = [self.get_category_data(queryset, 'inc'), self.get_category_data(queryset, 'exp')]
        serializer = self.get_serializer(global_list, many=True)
        return Response(serializer.data)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
