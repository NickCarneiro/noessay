import base64
from django.shortcuts import render_to_response
from search import request_utils
from search.models import Scholarship
from search.search_request import SearchRequest
from django.db.models import Q
from search.serp_result import SerpResult
from pyes import *

def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')
    search_req = SearchRequest(keyword, location)
    conn = ES('noessay.com:9200')

    query = TermQuery('title_and_description', keyword)
    results = conn.search(query=query)
    scholarships = []
    for scholarship in results:
        #print scholarship
        sid = scholarship.django_id
        sk = request_utils.encrypt_sid(str(sid))
        result = SerpResult(sk, scholarship)
        scholarships.append(result)
    return render_to_response('serp.html', {'scholarship_list': scholarships, 'search_request': search_req})