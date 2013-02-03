from django.contrib.localflavor.us.models import USStateField
from django.db import models
GENDER = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Other'),
    (3, 'None')
)

SCHOOL_STATUS = (
    (0, 'Public'),
    (1, 'Private nonprofit'),
    (2, 'For-profit')
)

class School(models.Model):
    city = models.CharField()
    state = USStateField()
    name = models.CharField()
    description = models.CharField()
    student_population = models.IntegerField()
    undergrad_tuition_resident = models.IntegerField()
    undergrad_tuition_nonresident = models.IntegerField()
    profit_status = models.CharField(choices=SCHOOL_STATUS)

# Create your models here.
class Scholarship(models.Model):
    title = models.CharField()
    description = models.CharField()
    deadline = models.DateField(blank=True)
    organization = models.CharField()
    age_restriction = models.SmallIntegerField(blank=True)
    state_restriction = USStateField(blank=True)
    essay_required = models.BooleanField()
    gpa_restriction = models.FloatField(blank=True)
    additional_restriction = models.CharField(blank=True)
    major_restriction = models.CharField(blank=True)
    college_restriction = models.OneToOneField(School, blank=True)
    #really should be enum of male, female, other, none
    gender_restriction = models.CharField(choices=GENDER)
    essay_length_words = models.IntegerField()
    third_party_url = models.URLField()
    amount_usd = models.IntegerField(blank=True)
    sponsored = models.BooleanField()





