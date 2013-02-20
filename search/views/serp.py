from django.shortcuts import render_to_response
from search.models import Scholarship
from search.search_request import SearchRequest
from django.db.models import Q
def serp(request):
    keyword = request.GET.get('q')
    location = request.GET.get('l')
    search_req = SearchRequest(keyword, location)

    scholarships = Scholarship.objects.filter(Q(title__icontains=search_req.keyword) or
                                                Q(description__icontains=search_req.keyword))
    return render_to_response('serp.html', {'scholarship_list': scholarships})