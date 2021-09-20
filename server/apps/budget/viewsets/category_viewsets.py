from django.db.models import Sum, Prefetch
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.budget.models import TransactionCategory, Transaction
from apps.budget.serializers import (
    TransactionCategoryCreateSerializer,
    TransactionCategoryListSerializer,
    TransactionCategorySumsSerializer
)
from apps.budget.filtersets import TransactionFilter
from apps.users.permissions import OwnerOnly


class TransactionCategoryViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                                 mixins.ListModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated, OwnerOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def total_amount(self, request):
        queryset = self.get_queryset()
        data = [{'total_amount': obj.transactions.aggregate(total_amount=Coalesce(Sum('amount'), .0))['total_amount'],
                 'id': obj.id,
                 'category_type': obj.category_type,
                 'name': obj.name} for obj in queryset]
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = TransactionCategory.objects.all()
        if self.action == 'total_amount':
            prefetch = Prefetch('transactions',
                                queryset=self.filter_queryset(Transaction.objects.filter(owner=self.request.user)))
            queryset = queryset.filter(owner=self.request.user).prefetch_related(prefetch)
        if self.action == 'list':
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_serializer_class(self):
        serializer = TransactionCategoryCreateSerializer
        if self.action == 'list':
            serializer = TransactionCategoryListSerializer
        if self.action == 'create':
            serializer = TransactionCategoryCreateSerializer
        if self.action == 'total_amount':
            serializer = TransactionCategorySumsSerializer
        return serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # disable filtering
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
