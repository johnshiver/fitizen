from django import forms

from .models import WeightExercise


class WeightExerciseForm(forms.ModelForm):

    level = forms.ChoiceField()

    class Meta:
        model = WeightExercise
        fields = ['level', 'set1', 'set2', 'set3']

    def __init__(self, *args, **kwargs):
        self.view_choices = kwargs.pop('view_choices')
        self.exercise = kwargs.pop('exercise')
        super(WeightExerciseForm, self).__init__(*args, **kwargs)
        self.fields['level'] = forms.ChoiceField(choices=self.view_choices)
        self.fields['set1'].initial=self.exercise[0].set1
        self.fields['set2'].initial=self.exercise[0].set2
        self.fields['set3'].initial=self.exercise[0].set3
        super(WeightExerciseForm, self).full_clean()
