from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic import CreateView, RedirectView, View, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from .forms import RegistrationForm, LoginForm


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Contact(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Register(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = "accounts/signup.html"


class Login(FormView):
    form_class = LoginForm
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
class Logout(RedirectView):
    # reverse lazy only works when class is instantiated
    # makes classes easier, no methods to overwrite
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)




