from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from search import request_utils
from search.models import Scholarship


def scholarship_redirect(request):
    sk = request.GET.get('sk')
    title = request.GET.get('title')
    if title:
        safe_title = title.encode('ascii', 'ignore')
    else:
        safe_title = ''
    redirect_url = '/scholarship/{}/?title={}'.format(sk, safe_title)
    return redirect(redirect_url, permanent=True)


def view_scholarship(request, scholarship_key):
    if not scholarship_key:
        scholarship_key = request.GET.get('sk')
    scholarship_id = request_utils.decrypt_sk(scholarship_key)

    scholarship = Scholarship.objects.get(id=scholarship_id)
    context = {'scholarship_model':ain. scholarship,
               'scholarship_key': scholarship_key,
               'page_title': scholarship.title
    }
    return render_to_response('view_scholarship.html',
                              context,
                              context_instance=RequestContext(request))