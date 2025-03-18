from django.db import models
from .constants import ACTIVITY_CHOICES

#The models are the representations of the database tables. They are used to interact with the database.
class Case(models.Model):
    """
    A model representing a case.

    Attributes:
        id (int): The primary key for the case.
    """
    id = models.AutoField(primary_key=True)
    avg_time = models.FloatField(default=0)
    type = models.CharField(max_length=25, default='None')
    branch = models.CharField(max_length=25, default='None')
    ramo = models.CharField(max_length=25, default='None')
    brocker = models.CharField(max_length=25, default='None')
    state = models.CharField(max_length=25, default='None')
    client = models.CharField(max_length=25, default='None')
    creator = models.CharField(max_length=25, default='None')
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"Case {self.id}"

class Activity(models.Model):
    """
    A model representing an activity related to a case.

    Attributes:
        id (int): The primary key for the activity.
        case (Case): The ID of the related case.
        timestamp (datetime): The timestamp of the activity.
        name (str): The name of the activity, chosen from ACTIVITY_CHOICES.
        case_index (int): The index of the case, with a default value of 0.
    """
    id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, related_name='activities', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=25)
    case_index = models.IntegerField(default=0)
    tpt = models.FloatField(default=0)

    def __str__(self):
        return f"{self.case.id} - {self.name} at {self.timestamp}"
    
class Variant(models.Model):
    """
    A model representing a variant.

    Attributes:
        id (int): The primary key for the variant.
        activities (str): The activities of the variant.
        cases (str): The cases of the variant.
    """
    id = models.AutoField(primary_key=True)
    activities = models.CharField(max_length=50)
    cases = models.CharField(max_length=50)
    number_cases = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    avg_time = models.FloatField(default=0)

    def __str__(self):
        return self.name