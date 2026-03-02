from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None  # remove username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # remove obrigatoriedade de username

    def __str__(self):
        return self.email
