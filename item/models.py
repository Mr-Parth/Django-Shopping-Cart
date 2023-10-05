from django.db import models
from django.contrib.auth.models import AbstractUser

class Item(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self) -> str:
        return self.product_name