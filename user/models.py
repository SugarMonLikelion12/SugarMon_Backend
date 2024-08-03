from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    username = models.CharField(max_length=100, unique = True)
    nickname = models.CharField(max_length=100)
    isDoctor = models.BooleanField()