from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager that uses email field as an identifier.
    """
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Email is required to create a user')
        if not username:
            raise ValueError('Username is required to create a user')
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('Email is required to create a user')
        if not username:
            raise ValueError('Username is required to create a user')
        user = self.model(email=email, username=username, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()
        return user
