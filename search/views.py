from django.shortcuts import render_to_response, redirect, render
from search.models import Scholarship

def home(request):
    return render_to_response('index.html')

#attempt to render nonexistent file to cause 500 error to make sure logs work
def error(request):
    return render_to_response('error.html')

def serp(request):
    scholarships = Scholarship.objects.all()
    return render_to_response('serp.html', {'scholarship_list': scholarships})

