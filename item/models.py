from django.db import models
from django.forms import ValidationError

def no_spaces_validator(value):
    if ' ' in value:
        raise ValidationError('Spaces are not allowed in this field.')

class Item(models.Model):
    product_identifier = models.CharField(max_length=255, unique=True, validators=[no_spaces_validator],db_index=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_identifier