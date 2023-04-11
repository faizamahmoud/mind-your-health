from django.db import models
from django.contrib.auth.models import User

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intake = models.FloatField(default=0, decimal_places=2) #in oz
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.intake} oz on {self.date} by {self.user.username}"
