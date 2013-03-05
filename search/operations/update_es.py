# MySQL is the master set of scholarships
# This script coeps them all into elasticsearch
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "noessay.settings")

from pyes import *
from pyes.mappings import *
from search.models import Scholarship

conn = ES('noessay.com:9200')
DEV_INDEX = 'noessay-dev'
PROD_INDEX = 'noessay-prod'
SCHOLARSHIP_TYPE = 'scholarship'

def create_index():
    try:
        conn.indices.delete_index(DEV_INDEX)
    except:
        pass

    conn.indices.create_index(DEV_INDEX)

    mapping = {
        'title': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        'third_party_url': {
            'index': 'no',
            'store': 'yes',
            'type': 'string'
        },
        'description': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        'date_added': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'date'
        },
        'deadline': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'date'
        },
        'essay_required': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'boolean'
        },
        'amount_usd': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'integer'
        },
        'organization': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        'min_age_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'integer'
        },
        'state_restriction': { # 2 letter postal code like TX
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        'essay_length_words': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'integer'
        },
        'gpa_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'float'
        },
        'additional_restriction': {
            'index': 'no',
            'store': 'yes',
            'type': 'string'
        },
        'major_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        # ensure that these values always come from the universities table
        'university_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        # ensure that these values always come from the Choices in models
        'ethnicity_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        # ensure that these values always come from the Choices in models
        'gender_restriction': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'string'
        },
        'sponsored': {
            'index': 'analyzed',
            'store': 'yes',
            'type': 'boolean'
        }
    }

    conn.indices.put_mapping(SCHOLARSHIP_TYPE, {'properties': mapping}, [DEV_INDEX])

def populate_index():
    #iterate over all the scholarships and put them in es index
    scholarships = Scholarship.objects.filter()
    for s in scholarships:
        print s.title
        university_name = None
        universities = s.university_restriction.all()
        if universities:
            university_name = universities[0]

        scholarship_es = {
            'title': s.title,
            'third_party_url': s.third_party_url,
            'description': s.description,
            'date_added': s.date_added,
            'deadline': s.deadline,
            'essay_required': s.essay_required,
            'amount_usd': s.amount_usd,
            'organization': s.organization,
            'min_age_restriction': s.min_age_restriction,
            'state_restriction': s.state_restriction,
            'essay_length_words': s.essay_required,
            'gpa_restriction': s.gpa_restriction,
            'additional_restriction': s.additional_restriction,
            'major_restriction': s.major_restriction,
            'university_restriction': university_name,
            'ethnicity_restriction': s.ethnicity_restriction,
            'gender_restriction': s.gender_restriction,
            'sponsored': s.sponsored
        }
        conn.index(scholarship_es, DEV_INDEX, SCHOLARSHIP_TYPE)


def query_index():
    q = TermQuery('description', 'black')
    results = conn.search(query=q)
    for r in results:
        print r



populate_index()
