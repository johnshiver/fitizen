from django.db import models
# from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime

# def validate_max(value):
#     if value > 500:
#         raise ValidationError(u'There is no way you did %s reps' % value)


class BodyWeightWorkout(models.Model):
    """
    Represents a single workout, assumes one workout per day
    """
    user = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(BodyWeightWorkout, self).save(*args, **kwargs)

    def __str__(self):
        if self.modified:
            return str(self.modified)
        else:
            return str(self.created)


class WeightExercise(models.Model):
    """
    Represents a single Exercise
    """
    PULLUP = 'PL'
    DIP = 'D'
    SQUAT = 'SQ'
    LSIT = 'LS'
    PUSHUP = 'PU'
    ROW = "RW"

    EXERCISE_CHOICES = (
        (PULLUP, 'Pullup'),
        (DIP, 'Dips'),
        (SQUAT, 'Sqat'),
        (LSIT, 'Senior'),
        (PUSHUP, 'Pushup'),
        (ROW, 'Row')
    )

    workout = models.ForeignKey(BodyWeightWorkout)
    exercise = models.CharField(max_length=2,
                                choices=EXERCISE_CHOICES)
    level = models.CharField(max_length=1, default='1')
    set1 = models.PositiveIntegerField(default=0)
    set2 = models.PositiveIntegerField(default=0)
    set3 = models.PositiveIntegerField(default=0)
