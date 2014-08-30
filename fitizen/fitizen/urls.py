from django.conf.urls import patterns, include, url

from django.contrib import admin
from profiles.views import CreateUser, DetailUser, Home, Contact
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact', Contact.as_view(), name='contact'),
    url(r'/user/(?P<pk>\d+)/$', DetailUser.as_view(), name="detail_user"),
    url(r'accounts/', include('authtools.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
