# system imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# services imports
from banking_app.managers import UserManager
from . import services


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "password",
    ]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(
        max_length=10, unique=True, default=services.generate_account_number
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    ip_address = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
