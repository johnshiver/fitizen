# from datetime import datetime

from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


from .models import BodyWeightWorkout

from braces import views


# Create your views here.
class CreateWorkout(
    views.LoginRequiredMixin,
    views.MessageMixin,
    RedirectView
):

    url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = request.user
        workout = BodyWeightWorkout(user=user)
        workout.save()
        self.messages.success("New workout created!")

        return super(CreateWorkout, self).get(request, *args, **kwargs)