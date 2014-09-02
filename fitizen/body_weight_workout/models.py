from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# def validate_max(value):
#     if value > 500:
#         raise ValidationError(u'There is no way you did %s reps' % value)


class BodyWeightWorkout(models.Model):
    """
    Represents a single workout, assumes one workout per day
    """
    user = models.ForeignKey(User, unique_for_date='date_created')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_created)


class WeightExercise(models.Model):
    """
    Represents a single Exercise
    """
    PULLUP = 'PU'
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

    SET_CHOICES = [(i, i) for i in range(1, 4)]

    workout = models.ForeignKey(BodyWeightWorkout)
    reps = models.PositiveSmallIntegerField()
    exercise = models.CharField(max_length=2,
                                choices=EXERCISE_CHOICES)
    which_set = models.IntegerField(choices=SET_CHOICES)
