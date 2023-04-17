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
