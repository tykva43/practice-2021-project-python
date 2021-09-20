import datetime

import factory
from apps.users.tests.factories import UserFactory


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.TransactionCategory'

    owner = factory.SubFactory(UserFactory)
    category_type = 'inc'
    name = 'test'


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'budget.Transaction'

    category = factory.SubFactory(TransactionCategoryFactory)
    owner = factory.SubFactory(UserFactory)
    date = datetime.datetime.now().date()
    amount = 1
