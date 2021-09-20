from django.contrib import admin

from apps.widgets.models import Widget


@admin.register(Widget)
class TransactionCategoryAdmin(admin.ModelAdmin):
    pass
