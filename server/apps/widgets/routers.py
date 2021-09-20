from rest_framework import routers

from apps.widgets.viewsets import WidgetViewSet

app_name = 'widgets'

router = routers.SimpleRouter()
router.register(r'', WidgetViewSet, basename='Widget')
urlpatterns = router.urls
