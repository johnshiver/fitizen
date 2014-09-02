from datetime import datetime

from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from .models import BodyWeightWorkout

from braces import views


# Create your views here.
class CreateWorkout(
    views.LoginRequiredMixin,
    views.MessageMixin,
    View
):

    url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        recent_workout = list(BodyWeightWorkout.objects.filter(user=request.user.id).datetimes('created', 'day', order='DESC')[:1])
        difference = (now - recent_workout[0])
        # check to see if they already worked out today
        if difference.days == 0:
            self.messages.success("You already worked out today!")
            return redirect('home')
        else:
            user = request.user
            workout = BodyWeightWorkout(user=user)
            workout.save()
            self.messages.success("New workout created!")
            return redirect('home')
