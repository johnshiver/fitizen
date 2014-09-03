from django.conf.urls import patterns, include, url

from django.contrib import admin
from profiles.views import Register, Home, Contact, Login, Logout
from body_weight_workout.views import CreateWorkout, WorkoutView, UpdateWorkout

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact', Contact.as_view(), name='contact'),
    url(r'^accounts/register/$', Register.as_view(), name='register'),
    url(r'^accounts/login/$', Login.as_view(), name='login'),
    url(r'^accounts/logout/$', Logout.as_view(), name='logout'),
    url(r'^create_workout/$', CreateWorkout.as_view(), name='create_workout'),
    url(r'^workout/(?P<workout_id>\d+)/$', WorkoutView.as_view(), name='view_workout'),
    url(r'^update_workout/(?P<workout_id>\d+)/(?P<group>\d+)/$', UpdateWorkout.as_view(), name='update_workout'),
    url(r'^admin/', include(admin.site.urls)),
)
