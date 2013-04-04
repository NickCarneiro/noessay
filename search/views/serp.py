from django.shortcuts import render_to_response
from noessay.settings import DEV_INDEX
from search import request_utils
from search.search_request import SearchRequest
from search.serp_result import SerpResult
from pyes import *
from search.models import *
from search.request_utils import *
from search.elasticsearch_fields import EsFields as es

ELASTICSEARCH_URL = 'noessay.com:9200'
DESCRIPTION_LENGTH = 300
PAGE_LENGTH = 10
def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')

    # refine params
    start = parse_int_param(request.GET.get('start'), 0)
    if start % PAGE_LENGTH != 0:
        start = 0
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
    search = Search(query, size=PAGE_LENGTH, start=start)
    search.add_highlight(es.description, fragment_size=300, number_of_fragments=5)
    results = conn.search(search, indices=DEV_INDEX)
    total_results = results.total
    scholarships = []
    for schol in results:
        sid = schol.django_id
        if schol._meta.highlight:
            schol.description = schol._meta.highlight['description'][0]
        else :
            schol.description = description_to_snippet(schol.description)
        sk = request_utils.encrypt_sid(str(sid))
        result = SerpResult(sk, schol)

        scholarships.append(result)
    build_pagination_objects(scholarships, total_results)
    return render_to_response('serp.html',
        {'scholarship_list': scholarships,
         'search_request': search_req,
         'result_count': total_results
        })

def description_to_snippet(desc):
    return desc[:DESCRIPTION_LENGTH].rsplit(' ', 1)[0] + '...'

def build_pagination_objects(scholarships, total_results):
    max_links = 10
    pages = total_results / PAGE_LENGTH
    links = []
    link_count = min(max_links, pages)
    current_page = link_count / 2
    for i in range(link_count):
        link = {
            url: '/'
        }
        links.add

