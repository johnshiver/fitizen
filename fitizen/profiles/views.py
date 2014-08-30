from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib import messages


from .models import Fitizen
from authtools.forms import UserCreationForm


class FormMessageMixin(object):

    @property
    def success_msg(self):
        return NotImplemented


class CreateUser(FormMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "base.html"

    success_msg = 'Account created!'


class DetailUser(DetailView):
    model = Fitizen
    template_name = "detail_user.html"
