from django.urls import path

from apps.users.views import UserCreateView, UserInfoView


urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user_registration'),
    path('me/', UserInfoView.as_view(), name='user_info'),
]
