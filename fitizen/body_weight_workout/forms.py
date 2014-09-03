from django import forms

from .models import WeightExercise


class WeightExerciseForm(forms.ModelForm):
    class Meta:
        model = WeightExercise
        fields = ['set1', 'set2', 'set3']
