from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique = True)
    nickname = models.CharField(max_length=100)
    isDoctor = models.BooleanField(default=False)