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
RESULTS_PER_PAGE = 10
def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')

    # refine params
    start = parse_int_param(request.GET.get('start'), 0)
    if start % RESULTS_PER_PAGE != 0:
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
    search = Search(query, size=RESULTS_PER_PAGE, start=start)
    search.add_highlight(es.description, fragment_size=300, number_of_fragments=5)
    results = conn.search(search, indices=DEV_INDEX)
    total_result_count = results.total
    scholarships = []
    for schol in results:
        sid = schol.django_id
        if schol._meta.highlight:
            schol.description = schol._meta.highlight['description'][0]
        else:
            schol.description = description_to_snippet(schol.description)
        sk = request_utils.encrypt_sid(str(sid))
        result = SerpResult(sk, schol)

        scholarships.append(result)
    page_links = build_pagination_objects(total_result_count, start, search_req)
    is_first_page = start == 0
    is_last_page = RESULTS_PER_PAGE + start >= total_result_count
    next_page_href = search_req.get_base_url(start + RESULTS_PER_PAGE)
    prev_page_href = search_req.get_base_url(start - RESULTS_PER_PAGE)
    return render_to_response('serp.html',
                              {
                                  'scholarship_list': scholarships,
                                  'search_request': search_req,
                                  'result_count': total_result_count,
                                  'page_links': page_links,
                                  'is_first_page': is_first_page,
                                  'is_last_page': is_last_page,
                                  'prev_page_href': prev_page_href,
                                  'next_page_href': next_page_href,
                                  'start_index': start + 1,
                                  'end_index': min(start + 1 + RESULTS_PER_PAGE, total_result_count),
                                  'results_per_page': RESULTS_PER_PAGE
                              }
    )


def description_to_snippet(desc):
    return desc[:DESCRIPTION_LENGTH].rsplit(' ', 1)[0] + '...'


def build_pagination_objects(result_count, start, search_req):
    if result_count == 0:
        return []
    if start % RESULTS_PER_PAGE != 0:
        start = 0
    # page numbers have to start at 1 because users are human
    current_page_number = start / RESULTS_PER_PAGE + 1
    # add non-link for current page
    links = [{'current_page': True, 'page_number': current_page_number, 'start': start}]
    # try to add up to 5 forward pages
    for i in range(1, 6):
        page_start = start + i * RESULTS_PER_PAGE
        if page_start >= result_count:
            break
        href = search_req.get_base_url(page_start)
        links.append({'current_page': False,
                      'page_number': current_page_number + i,
                      'start': page_start,
                      'href': href
        })
    # try to prepend 5 pages backward
    for i in range(1, 6):
        page_start = start - i * RESULTS_PER_PAGE
        if page_start < 0:
            break
        href = search_req.get_base_url(page_start)
        links.insert(0, {'current_page': False,
                         'page_number': current_page_number - i,
                         'start': page_start,
                         'href': href
        })
    return links

