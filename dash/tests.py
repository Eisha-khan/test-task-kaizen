from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dash.models import Item,Category
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_registration.api.views.base import BaseAPIView
from rest_registration.exceptions import LoginInvalid, UserNotFound
from rest_registration.settings import registration_settings
from collections import OrderedDict

test_item={"sku": "new","name": "NewItem","tags": "string","in_stock": 2,"availble_stock": 2,"category": "TestCat"}

def login(data):
    serializer = registration_settings.LOGIN_SERIALIZER_CLASS(data=data)
    serializer.is_valid(raise_exception=True)
    login_authenticator = registration_settings.LOGIN_AUTHENTICATOR
    user = login_authenticator(serializer.validated_data, serializer=serializer)
    auth_token_manager_cls = registration_settings.AUTH_TOKEN_MANAGER_CLASS
    auth_token_manager = auth_token_manager_cls()
    token = auth_token_manager.provide_token(user)
    return token
      

class ItemTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        token = login({"login":"testuser","password":"testpassword"})
        token = Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_item(self):
        """
        Ensure we can create a new Item.
        """
        url = '/items/'
        data=test_item
        #Create category first
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'NewItem')
    
    def test_list_items(self):
        """
        Ensure we can get Item list.
        """
        url = '/items/'

        #Create category/item first
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        self.client.post('/items/', test_item, format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_item(self):
        """
        Ensure we can update an Item.
        """
        data={"sku": "new","name": "UpdatedItem","tags": "string","in_stock": 2,"availble_stock": 2,"category": "TestCat"}
        #Create category/item first and get id
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        self.client.post('/items/', test_item, format='json')
        id=Item.objects.get().id
        url = f'/items/{id}/'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'UpdatedItem')

    def test_delete_item(self):
        """
        Ensure we can delete an Item.
        """
        #Create category/item first and get id
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        self.client.post('/items/', test_item, format='json')
        id=Item.objects.get().id
        url = f'/items/{id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)



class CategoryTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        token = login({"login":"testuser","password":"testpassword"})
        token = Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_category(self):
        """
        Ensure we can create a new Category.
        """
        url = '/categories/'
        data = {"name": "TestCat"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'TestCat')

    def test_list_category(self):
        """
        Ensure we can get Category list.
        """
        url = '/categories/'
        #create category first
        self.client.post(url, {"name": "TestCat"}, format='json')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_category(self):
        """
        Ensure we can update Category.
        """
        data={"name": "UpdatedCat"}
        #Create category/item first and get id
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        id=Category.objects.get().id
        url = f'/categories/{id}/'

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'UpdatedCat')

    def test_delete_category(self):
        """
        Ensure we can delete Category.
        """
        #Create category/item first and get id
        self.client.post('/categories/', {"name": "TestCat"}, format='json')
        id=Category.objects.get().id
        url = f'/categories/{id}/'
    
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 0)

    