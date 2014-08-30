from django.shortcuts import render
from django.views.generic import CreateView, DetailView, View
from django.contrib import messages
from django.http import HttpResponse


from .models import Fitizen
from authtools.forms import UserCreationForm


class TestHome(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateUser(CreateView):
    form_class = UserCreationForm
    template_name = "create.html"

    success_msg = 'Account created!'


class DetailUser(DetailView):
    model = Fitizen
    template_name = "detail_user.html"
