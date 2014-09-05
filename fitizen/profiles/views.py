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


def get_data(request):
    xdata = []
    ydata = []
    ydata2 = []
    ydata3 = []
    workouts = list(BodyWeightWorkout.objects.filter(user=request.user.id)[:5])
    xdata = range(len(workouts))
    #get pullups for each workout
    for workout in workouts:
        pullups = list(WeightExercise.objects.filter(workout=workout.id, exercise='PL'))
        print pullups[0].set1
        ydata.append(pullups[0].set1)
        ydata2.append(pullups[0].set2)
        ydata3.append(pullups[0].set3)
    return xdata, ydata, ydata2, ydata3


def demo_discretebarchart(request):
    """
    multibarchart page
    """
    # nb_element = 10
    # xdata = range(nb_element)
    # ydata = [random.randint(1, 10) for i in range(nb_element)]
    # ydata2 = map(lambda x: x * 2, ydata)
    # ydata3 = map(lambda x: x * 3, ydata)
    # ydata4 = map(lambda x: x * 4, ydata)

    xdata, ydata, ydata2, ydata3 = get_data(request)

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " reps"}}

    chartdata = {
        'x': xdata,
        'name1': 'set 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'set 2', 'y2': ydata2, 'extra2': extra_serie,
        'name3': 'set 3', 'y3': ydata3, 'extra3': extra_serie,
    }

    nb_element = 100
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                   "date_format": tooltip_date}

    date_chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarChart"
    chartcontainer = 'multibarchart_container'  # container name
    chartcontainer_with_date = 'date_multibarchart_container'  # container name
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
        'chartdata_with_date': date_chartdata,
        'chartcontainer_with_date': chartcontainer_with_date,
        'extra_with_date': {
            'name': chartcontainer_with_date,
            'x_is_date': True,
            'x_axis_format': '%d %b %Y',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }
    return render_to_response('test_chart.html', data)


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):

        """
        multibarchart page
        """

        xdata, ydata, ydata2, ydata3 = get_data(request)

        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " reps"}}

        chartdata = {
            'x': xdata,
            'name1': 'set 1', 'y1': ydata, 'extra1': extra_serie,
            'name2': 'set 2', 'y2': ydata2, 'extra2': extra_serie,
            'name3': 'set 3', 'y3': ydata3, 'extra3': extra_serie,
        }

        nb_element = 100
        start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
        xdata = range(nb_element)
        xdata = map(lambda x: start_time + x * 1000000000, xdata)
        ydata = [i + random.randint(1, 10) for i in range(nb_element)]
        ydata2 = map(lambda x: x * 2, ydata)

        tooltip_date = "%d %b %Y %H:%M:%S %p"
        extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                       "date_format": tooltip_date}

        date_chartdata = {
            'x': xdata,
            'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
            'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
        }

        charttype = "multiBarChart"
        chartcontainer = 'multibarchart_container'  # container name
        chartcontainer_with_date = 'date_multibarchart_container'  # container name
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
            'chartdata_with_date': date_chartdata,
            'chartcontainer_with_date': chartcontainer_with_date,
            'extra_with_date': {
                'name': chartcontainer_with_date,
                'x_is_date': True,
                'x_axis_format': '%d %b %Y',
                'tag_script_js': True,
                'jquery_on_ready': True,
            },
        }

        # workouts = BodyWeightWorkout.objects.filter(user=request.user.id).datetimes('created', 'day', order='DESC')
        workouts = BodyWeightWorkout.objects.filter(user=request.user.id)[:6]
        return render(request, self.template_name, {'workouts': workouts, 'data': data})


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
    success_url = reverse_lazy('home')
    model = User
    template_name = "accounts/signup.html"


class Login(
    views.AnonymousRequiredMixin,
    views.FormValidMessageMixin,
    FormView
):
    authenticated_redirect_url = reverse_lazy(u"home")
    form_class = LoginForm
    form_valid_message = "Logged in!"
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

