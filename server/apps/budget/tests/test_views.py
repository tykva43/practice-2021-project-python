from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.users.tests.factories import UserFactory
from .factories import TransactionCategoryFactory, TransactionFactory


class TransactionCategoryTests(APITestCase):
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
        template = 'budget:TransactionCategory-{}'
        if method in ['POST', 'GET']:
            return reverse(template.format('list'))
        elif method == 'DELETE':
            return reverse(template.format('detail'), args=[pk])

    def test_list_category_with_auth(self):
        """The user can get their data through a GET-request """
        # Create category for auth_user
        TransactionCategoryFactory.create(owner=self.auth_user)
        # Check if created category is returning
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_category_without_auth(self):
        """User cannot get another user's data through a GET-request """
        # Create category for unauth_user
        TransactionCategoryFactory(owner=self.unauth_user)
        # Create category for auth_user
        TransactionCategoryFactory(owner=self.auth_user)
        # Check if created category (where owner is unauth_user) is not returning
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_owner_destroy_category(self):
        """Owners can delete themselves categories via DELETE request"""
        # Create category with auth user as owner
        category = TransactionCategoryFactory(owner=self.auth_user)
        # Attempt to destroy authenticated user's category
        response = self.client.delete(path=self.get_path('DELETE', category.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_destroy_wrong_category(self):
        """The user cannot delete someone else's category via DELETE request"""
        category = TransactionCategoryFactory(owner=self.unauth_user)
        # Attempt to destroy another user's category
        response = self.client.delete(path=self.get_path('DELETE', category.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_create_category(self):
        """Status 201 is returned for a POST request with a correctly specified header data"""
        category_data = model_to_dict(TransactionCategoryFactory.build(), fields=['category_type', 'name'])
        response = self.client.post(path=self.get_path('POST'), data=category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauth_user_create_category(self):
        """Status 401 is returned for a POST request without Authentication param in query header"""
        # Clean auth header
        self.client.credentials()
        category_data = model_to_dict(TransactionCategoryFactory.build(), fields=['category_type', 'name'])
        response = self.client.post(path=self.get_path('POST'), data=category_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TransactionTests(APITestCase):
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
        template = 'budget:Transaction-{}'
        if method in ['POST', 'GET']:
            return reverse(template.format('list'))
        elif method in ['DELETE', 'PUT', 'PATCH']:
            return reverse(template.format('detail'), args=[pk])

    def test_list_transaction_with_auth(self):
        """The user can get their transaction data through a GET-request """
        # Create transaction for auth_user
        category = TransactionCategoryFactory(owner=self.auth_user)
        TransactionFactory(category=category, owner=self.auth_user)
        # Check if created transaction is returning
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_transaction_without_auth(self):
        """User cannot get another user's transaction data through a GET-request """
        # Create transaction for unauth_user
        category1 = TransactionCategoryFactory(owner=self.unauth_user)
        TransactionFactory(owner=self.unauth_user, category=category1)
        # Create transaction for auth_user
        category2 = TransactionCategoryFactory(owner=self.auth_user)
        TransactionFactory(owner=self.auth_user, category=category2)
        # Check if created transaction (where owner is unauth_user) is not returning
        response = self.client.get(path=self.get_path('GET'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_owner_destroy_transaction(self):
        """Owners can delete themselves transactions via DELETE request"""
        # Create transaction with auth_user as owner
        category = TransactionCategoryFactory(owner=self.auth_user)
        transaction = TransactionFactory(owner=self.auth_user, category=category)
        # Attempt to destroy authenticated user's transaction
        response = self.client.delete(path=self.get_path('DELETE', transaction.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_destroy_wrong_transaction(self):
        """The user cannot delete someone else's transaction via DELETE request"""
        category = TransactionCategoryFactory(owner=self.unauth_user)
        transaction = TransactionFactory(owner=self.unauth_user, category=category)
        # Attempt to destroy another user's transaction
        response = self.client.delete(path=self.get_path('DELETE', transaction.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_update_transaction(self):
        """Owners can update themselves transactions via PUT request"""
        category = TransactionCategoryFactory(owner=self.auth_user)
        transaction = TransactionFactory(owner=self.auth_user, category=category)
        transaction_data = model_to_dict(transaction, fields=['category', 'amount', 'date'])
        response = self.client.put(path=self.get_path('PUT', transaction.id), data=transaction_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_wrong_transaction(self):
        """The user cannot update someone else's transaction via PUT request"""
        category = TransactionCategoryFactory(owner=self.unauth_user)
        transaction = TransactionFactory(owner=self.unauth_user, category=category)
        transaction_data = model_to_dict(transaction, fields=['category', 'amount', 'date'])
        response = self.client.put(path=self.get_path('PUT', transaction.id), data=transaction_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_partial_update_transaction(self):
        """Owners can partial update themselves transactions via PATCH request"""
        category = TransactionCategoryFactory(owner=self.auth_user)
        transaction = TransactionFactory(owner=self.auth_user, category=category)
        transaction_data = model_to_dict(transaction, fields=['amount'])
        response = self.client.patch(path=self.get_path('PATCH', transaction.id), data=transaction_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_partial_update_wrong_transaction(self):
        """The user cannot partial update someone else's transaction via PATCH request"""
        category = TransactionCategoryFactory(owner=self.unauth_user)
        transaction = TransactionFactory(owner=self.unauth_user, category=category)
        transaction_data = model_to_dict(transaction, fields=['amount'])
        response = self.client.patch(path=self.get_path('PATCH', transaction.id), data=transaction_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_create_transaction(self):
        """Status 201 is returned for a POST request with a correctly specified header data"""
        data = model_to_dict(TransactionFactory.build(category=TransactionCategoryFactory(owner=self.auth_user)),
                             fields=['category', 'amount', 'date'])
        response = self.client.post(path=self.get_path('POST'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauth_user_create_transaction(self):
        """Status 401 is returned for a POST request without Authentication param in query header"""
        # Clean auth header
        self.client.credentials()
        data = model_to_dict(TransactionFactory.build(category=TransactionCategoryFactory(owner=self.unauth_user)),
                             fields=['category', 'amount', 'date'])
        response = self.client.post(path=self.get_path('POST'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
