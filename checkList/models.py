from django.db import models
from django.contrib.auth.models import User
from user.models import User
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Checklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    when = models.PositiveSmallIntegerField(default=False, validators=[MinValueValidator(0), MaxValueValidator(2)]) # 0부터 2까지만 입력 가능한 TINYINT 필드 (아침-점심-저녁)
    meal_order = models.BooleanField(default=False, verbose_name="식사 순서")
    sugar = models.BooleanField(default=False, verbose_name="식후 액상과당 섭취")
    exercise = models.BooleanField(default=False, verbose_name="운동 여부")

    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = date.today()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = "체크리스트"
        verbose_name_plural = "체크리스트들"

    # def __str__(self):
    #     return f"{self.user.username}님의 {self.date} 체크리스트"

