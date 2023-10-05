from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser  
User = CustomUser

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            "role": "user"
        }

    def test_register_user(self):
        response = self.client.post('/api/core/user/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        self.assertTrue(Token.objects.filter(user__username=self.user_data['username']).exists())

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

    def test_login_user(self):
        response = self.client.post('/api/core/user/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_login_user_failure_wrong_password_or_wrong_username(self):
        wrong_cred_user_data = self.user_data 
        wrong_cred_user_data["password"] = "wrongpass"
        response = self.client.post('/api/core/user/login/', wrong_cred_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        wrong_cred_user_data = self.user_data 
        wrong_cred_user_data["username"] = "wronguser"
        response = self.client.post('/api/core/user/login/', wrong_cred_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SuspendUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create(username='adminuser', is_staff=True)
        self.admin_user_2 = User.objects.create(username='adminuser2', is_staff=True)
        self.user = User.objects.create(username='testuser_to_suspend')
        self.user_2 = User.objects.create(username='testuser2_to_suspend')

    def test_suspend_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/core/user/suspend_user/{self.user.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_suspended)

    def test_suspend_user_failure_same_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/core/user/suspend_user/{self.admin_user.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_suspended)

    def test_suspend_user_failure_suspend_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/core/user/suspend_user/{self.admin_user_2.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_suspended)

    def test_suspend_user_failure_normal_user_suspending(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(f'/api/core/user/suspend_user/{self.admin_user_2.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_suspended)