from django.db import models
from .constants import ACTIVITY_CHOICES
class Case(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Case {self.id}"

class Activity(models.Model):
   
    case = models.ForeignKey(Case, related_name='activities', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=25, choices=ACTIVITY_CHOICES)

    def __str__(self):
        return f"{self.case.id} - {self.name} at {self.timestamp}"