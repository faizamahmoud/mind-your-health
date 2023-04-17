from django.urls import path
from .views import JournalEntryListCreateView, JournalEntryRetrieveUpdateDestroyView

urlpatterns = [
    path('journal/', JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
    path('journal/<int:pk>/', JournalEntryRetrieveUpdateDestroyView.as_view(), name='journal-entry-retrieve-update-destroy'),
]
