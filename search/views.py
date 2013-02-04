from django.shortcuts import render_to_response, redirect, render

def home(request):
    return render_to_response('index.html')

def error(request):
    return render_to_response('error.html')