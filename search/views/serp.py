import base64
from django.shortcuts import render_to_response
from search import request_utils
from search.models import Scholarship
from search.search_request import SearchRequest
from django.db.models import Q
from search.serp_result import SerpResult
from pyes import *
from search.models import *
from search.request_utils import *
from search.elasticsearch_fields import EsFields as es

ELASTICSEARCH_URL = 'noessay.com:9200'


def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')

    # refine params
    no_essay_required = parse_boolean_param(request.GET.get('ne'))
    deadline = parse_string_param(request.GET.get('d'), None)
    ethnicity = parse_int_param(request.GET.get('e'), None)
    gender = parse_int_param(request.GET.get('g'), None)
    refine = no_essay_required or deadline or ethnicity or gender

    search_req = SearchRequest(keyword, location, no_essay_required,
        deadline, ethnicity, gender)
    conn = ES(ELASTICSEARCH_URL)

    # empty query
    if not keyword and location == 'US':
        query = MatchAllQuery()

    # got a keyword but no state
    elif keyword and not refine and location and location == 'US':
        query = MultiMatchQuery(text=keyword, fields=[es.title, es.description])

    # got a keyword and a state
    elif keyword and not refine and location and location != 'US':
        multi_query = MultiMatchQuery(text=keyword, fields=[es.title, es.description])
        state_term_filter = TermFilter(es.state_restriction, location)
        query = FilteredQuery(multi_query, state_term_filter)

    # no keyword but a state
    elif not keyword and location and location != 'US':
        query = TermQuery(field=es.state_restriction, value=location)
    else:
        # got refine params
        refine_restrictions = []
        if no_essay_required:
            refine_restrictions.append({
                'term': { es.essay_required: False }
            })
        if deadline:
            refine_restrictions.append({
                'range': {
                    'deadline': {
                        'gte': deadline
                    }
                }
            })
        if ethnicity:
            ethnicity_string = ETHNICITIES[ethnicity]
            refine_restrictions.append({
                'term': { es.ethnicity_restriction: ethnicity_string}
            })
        if gender:
            gender_string = GENDER[gender]
            refine_restrictions.append({
                'term': { es.gender_restriction: gender_string}
            })

        query = {
            'filtered': {

                'query': {
                    'match_all': {}
                },
                'filter': {
                    'and': refine_restrictions
                }
            }
        }

    results = conn.search(query=query)
    scholarships = []
    for scholarship in results:
        #print scholarship
        sid = scholarship.django_id
        sk = request_utils.encrypt_sid(str(sid))
        result = SerpResult(sk, scholarship)
        scholarships.append(result)
    return render_to_response('serp.html',
        {'scholarship_list': scholarships,
         'search_request': search_req,
         'result_count': len(scholarships)
        })