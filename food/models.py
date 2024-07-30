from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from user.models import User

# Create your models here.
class AteFood(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name = "ateFood")
    name = models.CharField(max_length=100)
    ateDate = models.DateField()
    when = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)]) # 0부터 3까지만 입력 가능한 TINYINT 필드

    def save(self, *args, **kwargs):
        if self.ateDate is None:
            self.ateDate = date.today()
        super().save(*args, **kwargs)