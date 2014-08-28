from django.conf.urls import patterns, include, url

from django.contrib import admin
from profiles.views import TestView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TestView.as_view()),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
