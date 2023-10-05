from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import CustomUser 
from item.models import Item
from .models import CartItem

class CartItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='testuser')
        self.item = Item.objects.create(
            product_identifier='item1',
            display_name='Item 1',
            description='Description for Item 1',
            price=10000,
            stock=100,
        )
        self.cart_item = CartItem.objects.create(user=self.user, item=self.item, quantity=5)

    def test_list_user_cart_items(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user/cart/list_items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming only one item is in the cart
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['item']['product_identifier'], self.item.product_identifier)
        self.assertEqual(response.data[0]['quantity'], self.cart_item.quantity)

    def test_add_to_cart(self):
        self.client.force_authenticate(user=self.user)
        # Add 3 more items to the cart
        data = {'quantity': 3}  
        response = self.client.post(f'/api/user/cart/add_item/{self.item.product_identifier}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
         # Initial quantity (5) + added quantity (3)
        self.assertEqual(self.cart_item.quantity, 8) 

    def test_add_to_cart_failure(self):
        self.client.force_authenticate(user=self.user)
        # Add 3 more items to the cart
        data = {'quantity': 3}  
        response = self.client.post(f'/api/user/cart/add_item/random_product_name', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.cart_item.refresh_from_db()
        # Initial quantity (5) 
        self.assertEqual(self.cart_item.quantity, 5) 

    def test_remove_from_cart(self):
        self.client.force_authenticate(user=self.user)
        data = {'quantity': 2}  # Remove 2 items from the cart
        response = self.client.delete(f'/api/user/cart/remove_item/{self.item.product_identifier}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
        # Initial quantity (5) - removed quantity (2)
        self.assertEqual(self.cart_item.quantity, 3)  
        
        # Test removing the entire item from the cart
        data = {'quantity': 3}  # Remove the remaining 3 items from the cart
        response = self.client.delete(f'/api/user/cart/remove_item/{self.item.product_identifier}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Cart item should be deleted
        self.assertFalse(CartItem.objects.filter(user=self.user, item=self.item).exists())  

    def test_remove_from_cart_failiure_invalid_product_item(self):
        self.client.force_authenticate(user=self.user)
        data = {'quantity': 2}  # Remove 2 items from the cart
        response = self.client.delete(f'/api/user/cart/remove_item/random_product_name', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)  # Initial quantity (5)

    def test_remove_from_cart_removing_more_quantity_than_cart_quantity(self):
        self.client.force_authenticate(user=self.user)
        data = {'quantity': 10}  # Remove 2 items from the cart
        response = self.client.delete(f'/api/user/cart/remove_item/{self.item.product_identifier}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # For quantity more or equal to quantity in cart, delete entry
        self.assertFalse(CartItem.objects.filter(user=self.user, item=self.item).exists())   