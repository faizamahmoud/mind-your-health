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

    def test_date_label(self):
        intake = WaterIntake.objects.get(id=1)
        field_label = intake._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_user_label(self):
        intake = WaterIntake.objects.get(id=1)
        field_label = intake._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_intake_max_digits(self):
        intake = WaterIntake.objects.get(id=1)
        max_digits = intake._meta.get_field('intake').max_digits
        self.assertEquals(max_digits, 5)

    def test_object_name_is_intake_amount_and_date_and_username(self):
        intake = WaterIntake.objects.get(id=1)
        expected_object_name = f'{intake.intake} oz on {intake.date} by {intake.user.username}'
        self.assertEquals(expected_object_name, str(intake))