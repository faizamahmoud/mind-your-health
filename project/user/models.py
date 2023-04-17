from django.db import models
from water.models import WaterIntake
import datetime

class EndUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    water_drank_in_oz = models.ManyToManyField(WaterIntake) 
    journal_entries = models.ManyToManyField('JournalEntry')
    date = models.DateField(auto_now_add=True)


class JournalEntry(models.Model):
    author = models.ForeignKey(EndUser, on_delete=models.CASCADE, related_name='many_journal_entries')
    description = models.TextField()
    date = models.DateField(default=datetime.date.today)
    
   