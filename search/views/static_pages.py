from django.shortcuts import render_to_response

def about(request):
    return render_to_response('about.html')

def legal(request):
    return render_to_response('legal.html')