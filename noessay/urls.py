from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import search

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'search.views.home', name='home'),
    url(r'^search', 'search.views.serp', name='serp'),
    url(r'^about', 'search.views.about', name='about'),
    url(r'^legal', 'search.views.legal', name='legal'),
    url(r'^scholarship/', 'search.views.view_scholarship', name='serp'),
    url(r'^error', 'search.views.error', name='error'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the a   dmin:
    url(r'^admin/', include(admin.site.urls)),

    #SEO canonical urls
    url(r'^no-essay-scholarships', 'search.views.serp', name='serp'),
    url(r'^scholarships-in-texas', 'search.views.serp', name='serp'),


)
