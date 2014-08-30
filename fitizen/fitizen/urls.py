from django.conf.urls import patterns, include, url

from django.contrib import admin
from profiles.views import Register, Home, Contact, Login


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact', Contact.as_view(), name='contact'),
    url(r'^accounts/register/$', Register.as_view(), name='register'),
    url(r'^accounts/login/$', Login.as_view(), name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
