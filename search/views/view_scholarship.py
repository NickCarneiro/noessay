from django.shortcuts import render_to_response
from django.template import RequestContext
from search import request_utils
from search.models import Scholarship
def view_scholarship(request):
    scholarship_key = request.GET.get('sk')
    scholarship_id = request_utils.decrypt_sk(scholarship_key)

    scholarship = Scholarship.objects.get(id=scholarship_id)
    return render_to_response('view_scholarship.html',
                              {'scholarship_model': scholarship},
                              context_instance=RequestContext(request))