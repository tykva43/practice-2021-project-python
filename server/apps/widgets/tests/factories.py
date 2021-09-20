import datetime
import factory

from apps.users.tests.factories import UserFactory
from apps.budget.tests.factories import TransactionCategoryFactory

class WidgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'widgets.Widget'

    category = factory.SubFactory(TransactionCategoryFactory)
    owner = factory.SubFactory(UserFactory)
    money_limit = 1
    criterion = 'lt'
    validity = datetime.timedelta(days=1)
    color = '#000000'
    created_at = datetime.datetime.now()
