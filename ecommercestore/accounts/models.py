from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission, GroupManager, Group
from django.db import models

from ecommercestore.accounts.managers import PetstagramUserManager


class PetstagramUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = PetstagramUserManager()


class Customer(models.Model):
    CUSTOMER_NAME_MAX_LEN = 30

    name = models.CharField(
        max_length=CUSTOMER_NAME_MAX_LEN,
    )
    email = models.EmailField(
    )

    def __str__(self):
        return self.name

    description = models.TextField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        PetstagramUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )



