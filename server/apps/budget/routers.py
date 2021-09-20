from rest_framework import routers

from apps.budget.viewsets import TransactionCategoryViewSet, TransactionViewSet

app_name = 'budget'

router = routers.SimpleRouter()
router.register(r'category', TransactionCategoryViewSet, basename='TransactionCategory')
router.register(r'transaction', TransactionViewSet, basename='Transaction')
urlpatterns = router.urls
