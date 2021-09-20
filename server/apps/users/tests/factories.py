import factory
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'

    password = make_password('password')
    username = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.Sequence(lambda n: 'user%s@example.org' % n)
