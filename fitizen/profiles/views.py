from django.shortcuts import render
from django.views.generic import CreateView, DetailView, View
from django.contrib import messages
from django.http import HttpResponse


from .models import Fitizen
from authtools.forms import UserCreationForm


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Contact(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateUser(CreateView):
    form_class = UserCreationForm
    template_name = "create.html"

    success_msg = 'Account created!'


class DetailUser(DetailView):
    model = Fitizen
    template_name = "detail_user.html"
