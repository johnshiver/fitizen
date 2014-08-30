from django.db import models
from django.core.urlresolvers import reverse

from authtools.models import AbstractNamedUser


class Fitizen(AbstractNamedUser):

    def get_absolute_url(self):
        return reverse('detail_user', kwargs={"pk": self.pk})
