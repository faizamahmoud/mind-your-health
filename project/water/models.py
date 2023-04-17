from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intake = models.DecimalField(default=0, max_digits=5, decimal_places=2) # in oz
    date = models.DateField(auto_now_add=True)

    @classmethod
    def get_current_intake(cls, user):
        today = timezone.now().date()
        try:
            intake = cls.objects.get(user=user, date=today)
        except cls.DoesNotExist:
            intake = cls(user=user, intake=0)
        return intake

    def add_intake(self, amount):
        self.intake += amount
        self.save()

    @staticmethod
    def calculate_daily_water_goal(weight):
        daily_goal = weight * .5
        return daily_goal

    @property
    def remaining_intake(self):
        daily_goal = self.calculate_daily_water_goal(self.user.weight)
        return max(0, daily_goal - self.intake)
