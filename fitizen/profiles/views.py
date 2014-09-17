from __future__ import absolute_import

import random
import time
import datetime

from django.shortcuts import render, render_to_response
from django.views.generic import CreateView, RedirectView, View, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from .forms import RegistrationForm, LoginForm
from body_weight_workout.models import BodyWeightWorkout, WeightExercise

from braces import views


def fix_exercise(abbreviation):

    exercises = {
        'PL': 'Pullups',
        'D': 'Dips',
        'SQ': 'Squats',
        'LS': 'L-sits',
        'PU': "Pushups",
        'RW': "Rows"
    }
    return exercises[abbreviation]


def get_data(request, exercise='PL'):
    exercise = exercise
    xdata = []
    ydata = [0 for x in range(5)]
    ydata2 = [0 for x in range(5)]
    ydata3 = [0 for x in range(5)]
    if request.user.is_authenticated():
        workouts = list(BodyWeightWorkout.objects.filter(user=request.user.id).order_by('-modified')[:5])
    else:
        print 'where we are supposed to be'
        workouts = BodyWeightWorkout.objects.filter(user_id=23)

    # change this to dates at some point
    xdata = range(1, 6)
    # get reps for each workout
    i = 0
    for workout in workouts:
        pullups = list(WeightExercise.objects.filter(workout=workout.id, exercise=exercise))
        ydata[i] = pullups[0].set1
        ydata2[i] = pullups[0].set2
        ydata3[i] = pullups[0].set3
        i += 1
    return xdata, ydata, ydata2, ydata3


def return_chart_data(request, exercise='PL'):
    exercise = exercise
    xdata, ydata, ydata2, ydata3 = get_data(request, exercise=exercise)

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " reps"}}

    chartdata = {
        'x': xdata,
        'name1': 'set 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'set 2', 'y2': ydata2, 'extra2': extra_serie,
        'name3': 'set 3', 'y3': ydata3, 'extra3': extra_serie,
    }

    charttype = "multiBarChart"
    chartcontainer = 'multibarchart_container'  # container name

    workouts = None
    if request.user.is_authenticated():
        workouts = BodyWeightWorkout.objects.filter(user=request.user.id).order_by('-modified')[:5]

    exercise = fix_exercise(exercise)

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'workouts': workouts,
        'exercise': exercise,
    }

    return data


def demo_discretebarchart(request):
    """
    multibarchart page
    """

    data = return_chart_data(request, exercise='SQ')
    return render_to_response('test_chart.html', data)


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):

        if self.kwargs.get('exercise', None):
            exercise = self.kwargs['exercise']
        else:
            exercise = 'PL'
        data = return_chart_data(request, exercise=exercise)
        # recent workouts included in return_chart_data
        return render(request, self.template_name, data)


class Contact(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Register(
    views.AnonymousRequiredMixin,
    views.FormValidMessageMixin,
    CreateView
):
    authenticated_redirect_url = reverse_lazy(u"home")
    form_class = RegistrationForm
    form_valid_message = 'Thanks for signing up, go ahead and login'
    success_url = reverse_lazy('login')
    model = User
    template_name = "accounts/signup.html"


class Login(
    views.AnonymousRequiredMixin,
    # views.FormValidMessageMixin,
    FormView
):
    authenticated_redirect_url = reverse_lazy(u"home")
    form_class = LoginForm
    # sform_valid_message = "Logged in!"
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # check to see if username and password match
        user = authenticate(username=username, password=password)

        # if they match, user is logged in with a cookie
        # redirects to success url, which we said is the homepage
        if user is not None and user.is_active:
            login(self.request, user)
            return super(Login, self).form_valid(form)
        else:
            return self.form_invalid(form)


# a redirect view...redirects!
class Logout(
    views.LoginRequiredMixin,
    views.MessageMixin,
    RedirectView
):
    # reverse lazy only works when class is instantiated
    # makes classes easier, no methods to overwrite
    url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(Logout, self).get(request, *args, **kwargs)

