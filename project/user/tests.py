from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date
from .models import JournalEntry, WaterIntake
from .serializers import JournalEntrySerializer, WaterIntakeSerializer


USER_CREATE_URL = reverse('user-create')
TOKEN_CREATE_URL = reverse('token-create')
JOURNAL_ENTRY_URL = reverse('journal-entry-list-create')
WATER_INTAKE_URL = reverse('water-intake-create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AuthenticatedAPITest(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test@test.com',
            password='testpassword123',
            first_name='John',
            last_name='Doe',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class JournalEntryAPITest(AuthenticatedAPITest):

    def test_create_journal_entry(self):
        """Test creating a new journal entry"""
        payload = {
            'description': 'This is a test journal entry',
            'date': date.today(),
        }
        res = self.client.post(JOURNAL_ENTRY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        entry = JournalEntry.objects.get(id=res.data['id'])
        self.assertEqual(payload['description'], entry.description)
        self.assertEqual(payload['date'], str(entry.date))
        self.assertEqual(entry.user, self.user)

    def test_retrieve_journal_entry(self):
        """Test retrieving a journal entry"""
        entry = JournalEntry.objects.create(
            user=self.user,
            description='Test entry',
            date=date.today(),
        )
        url = reverse('journal-entry-retrieve-update-destroy', args=[entry.id])
        res = self.client.get(url)

        serializer = JournalEntrySerializer(entry)
        self.assertEqual(res.data, serializer.data)

    def test_update_journal_entry(self):
        """Test updating a journal entry"""
        entry = JournalEntry.objects.create(
            user=self.user,
            description='Test entry',
            date=date.today(),
        )
        url = reverse('journal-entry-retrieve-update-destroy', args=[entry.id])
        payload = {'description': 'Updated test entry'}
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        entry.refresh_from_db()
        self.assertEqual(entry.description, payload['description'])

    def test_delete_journal_entry(self):
        """Test deleting a journal entry"""
        entry = JournalEntry.objects.create(
            user=self.user,
            description='Test entry',
            date=date.today(),
        )
        url = reverse('journal-entry-retrieve-update-destroy', args=[entry.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(JournalEntry.DoesNotExist):
            entry.refresh_from_db()


class WaterIntakeAPITest(AuthenticatedAPITest):

    def test_create_water_intake(self):
        """Test creating a new water intake"""
        payload = {'intake': 50}
        res = self.client.post(WATER_INTAKE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        intake = WaterIntake.objects.get(id=res.data['id'])
        self.assertEqual(intake.intake, payload['intake'])
        self.assertEqual(intake.user, self.user)

    def test_retrieve_water_intake(self):
        """Test retrieving water intake"""
        intake = WaterIntake.objects.create(user=self.user, intake=50)
        url = reverse
