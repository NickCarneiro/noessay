from django.shortcuts import render_to_response
from search.models import Scholarship

def serp(request):
    scholarships = Scholarship.objects.all()
    return render_to_response('serp.html', {'scholarship_list': scholarships})