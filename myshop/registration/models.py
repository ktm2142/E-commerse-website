from django.contrib.auth import get_user_model, user_logged_out
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, user_logged_out
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$',
                           message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        ],
        default='')
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.username


