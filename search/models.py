from django.contrib.localflavor.us.models import USStateField
from django.contrib import admin
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


class University(models.Model):
    homepage_url = models.URLField()
    city = models.CharField(max_length=100)
    state = USStateField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    student_population = models.IntegerField()
    undergrad_tuition_resident = models.IntegerField()
    undergrad_tuition_nonresident = models.IntegerField()
    profit_status = models.SmallIntegerField(choices=PROFIT_STATUS)

    def __unicode__(self):
        return self.name

# Create your models here.
class Scholarship(models.Model):
    third_party_url = models.URLField()
    title = models.CharField(max_length=400)
    description = models.TextField()
    date_added = models.DateField()
    deadline = models.DateField(blank=True)
    essay_required = models.BooleanField()
    amount_usd = models.IntegerField(blank=True)
    organization = models.CharField(max_length=200)
    min_age_restriction = models.SmallIntegerField(blank=True)
    state_restriction = USStateField(blank=True)
    essay_length_words = models.IntegerField(blank=True)
    gpa_restriction = models.FloatField(blank=True)
    additional_restriction = models.TextField(blank=True)
    major_restriction = models.CharField(max_length=100, blank=True)
    university_restriction = models.OneToOneField(University, blank=True)
    gender_restriction = models.SmallIntegerField(choices=GENDER, blank=True)
    sponsored = models.BooleanField()

    def __unicode__(self):
        return self.title

# make models available in admin
admin.site.register(University)
admin.site.register(Scholarship)


