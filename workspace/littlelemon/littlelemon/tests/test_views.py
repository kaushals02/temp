from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import Menu
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from restaurant.serializers import MenuSerializer
from rest_framework.authtoken.models import Token

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and get the token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create menu items
        self.burger = Menu.objects.create(title="Burger", price=50, inventory=200)
        self.pizza = Menu.objects.create(title="Pizza", price=100, inventory=150)
        self.salad = Menu.objects.create(title="Salad", price=30, inventory=300)

    def test_getall(self):
        response = self.client.get(reverse('menu-items'))
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
