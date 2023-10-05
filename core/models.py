from django.db import models
from django.contrib.auth.models import AbstractUser

# Core Models of this project - UserProfile and Item

class CustomUser(AbstractUser):
    is_suspended = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("user", "User")])

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()