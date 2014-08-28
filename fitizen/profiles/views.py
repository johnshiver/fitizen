from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TestView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = "base.html"
