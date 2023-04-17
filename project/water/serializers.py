from rest_framework import serializers
from .models import WaterIntake

class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['intake']

    def update(self, instance, validated_data):
        intake = validated_data.get('intake', instance.intake)
        if intake < 0:
            raise serializers.ValidationError("Intake amount cannot be negative.")
        instance.intake = intake
        instance.save()
        return instance



from django.test import TestCase
from django.contrib.auth.models import User
from .models import WaterIntake

class WaterIntakeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpass')
        WaterIntake.objects.create(user=user, intake=50.0)

    def test_intake_label(self):
        intake = WaterIntake.objects.get(id=1)
        field_label = intake._meta.get_field('intake').verbose_name
        self.assertEquals(field_label, 'intake')
        print(f"Intake label test passed for {intake}")

    def test_date_label(self):
        intake = WaterIntake.objects.get(id=1)
        field_label = intake._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')
        print(f"Date label test passed for {intake}")

    def test_user_label(self):
        intake = WaterIntake.objects.get(id=1)
        field_label = intake._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
        print(f"User label test passed for {intake}")

    def test_intake_max_digits(self):
        intake = WaterIntake.objects.get(id=1)
        max_digits = intake._meta.get_field('intake').max_digits
        self.assertEquals(max_digits, 5)
        print(f"Intake max digits test passed for {intake}")

    def test_object_name_is_intake_amount_and_date_and_username(self):
        intake = WaterIntake.objects.get(id=1)
        expected_object_name = f'{intake.intake} oz on {intake.date} by {intake.user.username}'
        self.assertEquals(expected_object_name, str(intake))
        print(f"Object name test passed for {intake}")

    def test_calculate_daily_water_goal(self):
        user = User.objects.get(username='testuser')
        daily_goal = WaterIntake.calculate_daily_water_goal(user.weight)
        self.assertEquals(daily_goal, 80.0)
        print(f"Daily water goal test passed for user {user}")

    def test_get_current_intake_existing(self):
        user = User.objects.get(username='testuser')
        intake = WaterIntake.get_current_intake(user)
        self.assertEquals(intake.intake, 50.0)
        print(f"Get current intake existing test passed for user {user}")

    def test_get_current_intake_non_existing(self):
        user = User.objects.create_user(username='testuser2', password='testpass')
        intake = WaterIntake.get_current_intake(user)
        self.assertEquals(intake.intake, 0)
        print(f"Get current intake non-existing test passed for user {user}")

    def test_add_intake(self):
        user = User.objects.get(username='testuser')
        intake = WaterIntake.get_current_intake(user)
        intake.add_intake(30.0)
        updated_intake = WaterIntake.get_current_intake(user)
        self.assertEquals(updated_intake.intake, 80.0)
        print(f"Add intake test passed for user {user}")

    def test_remaining_intake(self):
        user = User.objects.get(username='testuser')
        intake = WaterIntake.get_current_intake(user)
        intake.add_intake(30.0)
        remaining_intake = intake.remaining_intake
        self.assertEquals(remaining_intake, 0)
        print(f"Remaining intake test passed for user {user}")


from rest_framework import generics, permissions
from .models import WaterIntake
from .serializers import WaterIntakeSerializer
from datetime import date

    
class WaterIntakeView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = WaterIntakeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user, date=date.today())


    def perform_create(self, serializer):
        water_drunk = float(self.request.data.get('intake')) # assuming the frontend sends the amount of water as a float in the 'intake' field
        daily_goal = self.request.user.calculate_daily_water_goal()
        current_intake = sum([w.intake for w in self.request.user.waterintake_set.all()])

        if current_intake + water_drunk > daily_goal:
            # Handle the case where the user drinks more than their daily goal
            serializer.save(user=self.request.user, intake=daily_goal-current_intake)
        else:
            serializer.save(user=self.request.user)

        # Add the amount of water the user drank to their current intake
        current_intake += water_drunk
        self.request.user.update_current_water_intake(current_intake)

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
