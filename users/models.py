from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # espaço pra futuro: telefone, cpf, etc.
    # phone = models.CharField(max_length=20, blank=True)
    pass
