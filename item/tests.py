from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import CustomUser
from .models import Item 

User = CustomUser

class ItemViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='user',
            password='userpassword',
        )
        self.item_data = {
            'product_identifier': 'item1',
            'display_name': 'Item 1',
            'description': 'Description 1',
            'price': '1000',
            'stock': '100',
        }
        self.item = Item.objects.create(**self.item_data)

    def test_add_item(self):
        self.client.force_authenticate(user=self.admin_user)
        self.item_data = {
            'product_identifier': 'item_new',
            'display_name': 'Item',
            'description': 'Description 1',
            'price': '1000',
            'stock': '100',
        }
        response = self.client.post('/api/item/add_item/', self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_items_bulk(self):
        self.client.force_authenticate(user=self.admin_user)
        item_data_list = [
            {
                'product_identifier': 'item2',
                'display_name': 'Item 2',
                'description': 'Description 2',
                'price': '15.99',
                'stock': '200',
            },
            {
                'product_identifier': 'item3',
                'display_name': 'Item 3',
                'description': 'Description 3',
                'price': '10000',
                'stock': '300',
            },
        ]
        response = self.client.post('/api/item/add_items/', item_data_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_item(self):
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {
            'product_identifier': 'item1',
            'display_name': 'Item 1 Updated',
            'description': 'Updated Description',
            'price': '8000',
            'stock': '50',
        }
        response = self.client.put(f'/api/item/edit_item/{self.item.id}', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.display_name, updated_data['display_name'])

    def test_delete_item(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/item/delete_item/{self.item.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())