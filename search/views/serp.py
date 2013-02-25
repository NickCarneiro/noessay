import base64
from django.shortcuts import render_to_response
from search import request_utils
from search.models import Scholarship
from search.search_request import SearchRequest
from django.db.models import Q
from search.serp_result import SerpResult

def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')
    search_req = SearchRequest(keyword, location)

    scholarship_models = Scholarship.objects.filter(Q(title__icontains=search_req.keyword) |
                                                Q(description__icontains=search_req.keyword) |
                                                Q(organization__icontains=search_req.keyword))
    scholarships = []
    for scholarship in scholarship_models:
        sid = scholarship.id
        sk = request_utils.encrypt_sid(str(sid))
        result = SerpResult(sk, scholarship)
        scholarships.append(result)
    return render_to_response('serp.html', {'scholarship_list': scholarships, 'search_request': search_req})