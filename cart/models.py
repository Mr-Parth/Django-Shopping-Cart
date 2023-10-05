from django.db import models
from core.models import CustomUser
from item.models import Item

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)   

    def __str__(self) -> str:
        return f"{self.user.username}-{self.item.product_identifier}"