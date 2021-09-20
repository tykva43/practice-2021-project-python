from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.users.tests.factories import UserFactory
from apps.budget.tests.factories import TransactionCategoryFactory
from .factories import WidgetFactory


class WidgetsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create tests users"""
        cls.auth_user = UserFactory()
        cls.unauth_user = UserFactory()
        cls.client = APIClient()

    def setUp(self):
        """Authenticate test user"""

        def _get_jwt_token(user_credentials):
            url_token_auth = reverse('token_obtain_pair')
            response = self.client.post(url_token_auth, user_credentials, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            return response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(_get_jwt_token({'email': self.auth_user.email,
                                                                                   'password': 'password'})))

    def get_path(self, method, pk=None):
        template = 'widgets:Widget-{}'
        if method in ['POST', 'GET']:
            return reverse(template.format('list'))
        elif method == 'DELETE':
            return reverse(template.format('detail'), args=[pk])

    def test_list_widgets_with_auth(self):
        """The user can get their widgets data through a GET-request """
        WidgetFactory(owner=self.auth_user, category=TransactionCategoryFactory(owner=self.auth_user))
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_widgets_without_auth(self):
        """User cannot get another user's widgets data through a GET-request """
        WidgetFactory(owner=self.unauth_user, category=TransactionCategoryFactory(owner=self.unauth_user))
        WidgetFactory(owner=self.auth_user, category=TransactionCategoryFactory(owner=self.auth_user))
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_owner_destroy_widget(self):
        """Owners can delete themselves widgets via DELETE request"""
        widget = WidgetFactory(owner=self.auth_user, category=TransactionCategoryFactory(owner=self.auth_user))
        response = self.client.delete(path=self.get_path('DELETE', widget.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_destroy_wrong_widget(self):
        """The user cannot delete someone else's widget via DELETE request"""
        widget = WidgetFactory(owner=self.unauth_user, category=TransactionCategoryFactory(owner=self.unauth_user))
        response = self.client.delete(path=self.get_path('DELETE', widget.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_create_widget(self):
        """Status 201 is returned for a POST request with a correctly specified header data"""
        data = model_to_dict(WidgetFactory.build(category=TransactionCategoryFactory(owner=self.auth_user)),
                             fields=['category', 'money_limit', 'criterion', 'validity', 'color', 'created_at'])
        response = self.client.post(path=self.get_path('POST'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauth_user_create_widget(self):
        """Status 401 is returned for a POST request without Authentication param in query header"""
        self.client.credentials()
        data = model_to_dict(WidgetFactory.build(category=TransactionCategoryFactory(owner=self.unauth_user)),
                             fields=['category', 'money_limit', 'criterion', 'validity', 'color', 'created_at'])
        response = self.client.post(path=self.get_path('POST'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
