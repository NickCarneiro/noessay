from django.contrib.localflavor.us.models import USStateField
from django.db import models
GENDER = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Other'),
    (3, 'None')
)

PROFIT_STATUS = (
    (0, 'Public'),
    (1, 'Private nonprofit'),
    (2, 'For-profit')
)

class School(models.Model):
    city = models.CharField(max_length=100)
    state = USStateField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    student_population = models.IntegerField()
    undergrad_tuition_resident = models.IntegerField()
    undergrad_tuition_nonresident = models.IntegerField()
    profit_status = models.SmallIntegerField(choices=PROFIT_STATUS)

# Create your models here.
class Scholarship(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    deadline = models.DateField(blank=True)
    organization = models.CharField(max_length=200)
    age_restriction = models.SmallIntegerField(blank=True)
    state_restriction = USStateField(blank=True)
    essay_required = models.BooleanField()
    gpa_restriction = models.FloatField(blank=True)
    additional_restriction = models.TextField(blank=True)
    major_restriction = models.CharField(max_length=100, blank=True)
    college_restriction = models.OneToOneField(School, blank=True)
    #really should be enum of male, female, other, none
    gender_restriction = models.SmallIntegerField(choices=GENDER)
    essay_length_words = models.IntegerField()
    third_party_url = models.URLField()
    amount_usd = models.IntegerField(blank=True)
    sponsored = models.BooleanField()





