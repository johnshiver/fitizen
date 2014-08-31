from django.db import models
from django.conf import settings


class BodyWeightWorkout(models.Model):
    """
    Represents a single workout, assumes one workout per day
    """
    user = owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)
