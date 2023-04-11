from django.db import models
from django.contrib.auth.models import User

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intake = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
