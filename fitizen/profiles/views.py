from django.shortcuts import render, response
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView
from django.contrib import messages

from authtools.models import AbstractEmailUser
from authtools.forms import UserCreationForm


class FormMessageMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return response("detail_user")


class CreateUser(FormMessageMixin, CreateView):
    form_class = UserCreationForm
    model = AbstractEmailUser
    template_name = "base.html"

    success_msg = 'Account created!'


class DetailUser(DetailView):
    model = AbstractEmailUser
    template_name = "detail_user.html"
