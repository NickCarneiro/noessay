class CanonicalUrlMiddleware(object):
    def process_request(self, request):
        if 'scholarships-in-texas' in request.path:
            request.GET = request.GET.copy()
            request.GET['q'] = ''
            request.GET['l'] = 'TX'