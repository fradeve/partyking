from django.conf.urls import patterns, include, url
from django.contrib import admin
from partyking.apps.core import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'partyking.views.home', name='home'),
    # url(r'^partyking/', include('partyking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.chart),
    url(r'^vote/', views.vote),
    url(r'^login/vote/', views.vote),
    url(r'addvote/$', views.addvote),
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
