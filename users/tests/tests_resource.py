import uuid
from typing import Dict, Union

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class UserTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the whole TestCase. Note: Make a copy of the data before modifying it. """

        cls.data: Dict[str, Union[str, None, bool]] = {
            "username": "test",
            "first_name": "Test",
            "last_name": "T",
            "email": "test@mail.com",
            "mobile_number": "1234567890",
            "password": "test@123",
            "avatar": None,
            "dob": "1993-08-20",
            "gender": "M",
            "is_active": False
        }

        cls.partial_data: Dict[str, Union[bool, str]] = {
            'is_active': True
        }

    def __user_create(self, data: Union[dict, None] = None) -> User:
        """
        Crate a user
        :param data: dict
        :return:
        """
        data = data if data is not None else self.data
        return User.objects.create(**data)

    def __user_bulk_create(self, batch_count: int = 2) -> None:
        """
        Create bulk users
        :type batch_count: int
        """
        data = self.data.copy()
        del data['username']

        users = [User(username='test' + str(value), **data) for value in range(batch_count)]
        User.objects.bulk_create(users)

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('users:user-list')
        data = self.data.copy()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertIn('id', response.data.get('data'))
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_empty_data(self):
        """
        Ensure we are getting error while creating a new user object with empty data.
        """
        url = reverse('users:user-list')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_create_user_with_empty_username(self):
        """
        Ensure we are getting error while creating a new user object with empty username.
        """
        url = reverse('users:user-list')
        data = self.data.copy()
        data['username'] = ""
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_create_user_with_empty_exist_username(self):
        """
        Ensure we are getting error while creating a new user object with already exist username.
        """
        self.__user_create()

        url = reverse('users:user-list')
        data = self.data.copy()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_list_user(self):
        """
        Ensure we can get the list of user object.
        """
        self.__user_bulk_create()

        url = reverse('users:user-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertIsNotNone(response.data.get('data').get('results'))
        self.assertEquals(len(response.data.get('data').get('results')), 2)
        self.assertEquals(response.data.get('data').get('count'), 2)
        self.assertIsNone(response.data.get('data').get('next'))
        self.assertIsNone(response.data.get('data').get('previous'))
        self.assertEqual(User.objects.count(), 2)

    def test_list_user_with_pagination_params(self):
        """
        Ensure we can get the list of user object with pagination params.
        """
        self.__user_bulk_create()

        url = reverse('users:user-list')
        params = {'limit': 1, 'offset': 0}
        response = self.client.get(url, params, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertIsNotNone(response.data.get('data').get('results'))
        self.assertEquals(len(response.data.get('data').get('results')), 1)
        self.assertEquals(response.data.get('data').get('count'), 2)
        self.assertIsInstance(response.data.get('data').get('next'), str)
        self.assertIsNone(response.data.get('data').get('previous'))
        self.assertEqual(User.objects.count(), 2)

    def test_list_user_with_empty_results(self):
        """
        Ensure we can get the list of user object with pagination params.
        """
        self.__user_bulk_create()

        url = reverse('users:user-list')
        params = {'limit': 1, 'offset': 2}
        response = self.client.get(url, params, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertIsNotNone(response.data.get('data').get('results'))
        self.assertEquals(len(response.data.get('data').get('results')), 0)
        self.assertEquals(response.data.get('data').get('count'), 2)
        self.assertIsNone(response.data.get('data').get('next'))
        self.assertIsInstance(response.data.get('data').get('previous'), str)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertEqual(response.data.get('data').get('id'), str(user.id))
        self.assertEqual(User.objects.count(), 1)

    def test_retrieve_user_with_non_exist_pk(self):
        """
        Ensure we can retrieve a user object.
        """
        url = reverse('users:user-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))
        self.assertEqual(User.objects.count(), 0)

    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.data.copy()
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertEqual(response.data.get('data').get('id'), str(user.id))
        self.assertEqual(User.objects.count(), 1)

    def test_update_user_with_non_exist_pk(self):
        """
        Ensure we can update a user object.
        """
        url = reverse('users:user-detail', kwargs={'pk': uuid.uuid4()})
        data = self.data.copy()
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))
        self.assertEqual(User.objects.count(), 0)

    def test_update_user_with_empty_data(self):
        """
        Ensure we are getting error while updating a user object with empty data.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = {}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_update_user_with_empty_username(self):
        """
        Ensure we are getting error while updating a user object with empty username.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.data.copy()
        data['username'] = ""
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_update_user_with_empty_exist_username(self):
        """
        Ensure we are getting error while updating a user object with already exist username.
        """
        self.__user_create()

        data2 = self.data.copy()
        data2['username'] = 'test2'
        user = self.__user_create(data2)

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.data.copy()
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_partial_update_user(self):
        """
        Ensure we can update a user object.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.partial_data.copy()
        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertEqual(response.data.get('data').get('id'), str(user.id))
        self.assertEqual(User.objects.count(), 1)

    def test_partial_update_user_with_non_exist_pk(self):
        """
        Ensure we can update a user object.
        """
        url = reverse('users:user-detail', kwargs={'pk': uuid.uuid4()})
        data = self.partial_data.copy()
        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))
        self.assertEqual(User.objects.count(), 0)

    def test_partial_update_user_with_empty_data(self):
        """
        Ensure we can updating a user object with empty data.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = {}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('errors'))
        self.assertEqual(response.data.get('data').get('id'), str(user.id))
        self.assertEqual(User.objects.count(), 1)

    def test_partial_update_user_with_empty_username(self):
        """
        Ensure we are getting error while updating a user object with empty username.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.partial_data.copy()
        data['username'] = ""
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_partial_update_user_with_empty_exist_username(self):
        """
        Ensure we are getting error while updating a user object with already exist username.
        """
        self.__user_create()

        data2 = self.data.copy()
        data2['username'] = 'test2'
        user = self.__user_create(data2)

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        data = self.partial_data.copy()
        data['username'] = 'test'
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))

    def test_destroy_user(self):
        """
        Ensure we can delete a user object.
        """
        user = self.__user_create()

        url = reverse('users:user-detail', kwargs={'pk': user.pk})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_destroy_user_with_non_exist_pk(self):
        """
        Ensure we can delete a user object.
        """
        url = reverse('users:user-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('data', response.data)
        self.assertIn('errors', response.data)
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('errors'))
        self.assertEqual(User.objects.count(), 0)
