from django.contrib import admin

from apps.budget.models import Transaction, TransactionCategory


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    pass
