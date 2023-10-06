from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Core Models of this project - UserProfile and CustomUser
class CustomUser(AbstractUser):
    is_suspended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.username


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = "user"
        if instance.is_staff:
            role = "admin"
        UserProfile.objects.create(user=instance, role=role)
