from django.shortcuts import render_to_response
from django.conf import settings

def home(request):
    return render_to_response('index.html', {'environment': settings.ENVIRONMENT})