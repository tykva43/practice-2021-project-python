from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt import authentication

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserInfoSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserInfoView(RetrieveAPIView):
    serializer_class = UserInfoSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
