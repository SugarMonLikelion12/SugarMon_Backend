from django.db import models
from user.models import User

# Create your models here.
class gIndex(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name = "gIndex")
    foodName = models.CharField(max_length=30)
    gIndex = models.FloatField()