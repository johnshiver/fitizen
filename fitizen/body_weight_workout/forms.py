from django import forms

from .models import WeightExercise


class WeightExerciseForm(forms.ModelForm):

    level = forms.ChoiceField()

    class Meta:
        model = WeightExercise
        fields = ['level', 'set1', 'set2', 'set3']

    def __init__(self, *args, **kwargs):
        self.view_choices = kwargs.pop('view_choices')
        super(WeightExerciseForm, self).__init__(*args, **kwargs)
        self.fields['level'] = forms.ChoiceField(choices=self.view_choices)

        super(WeightExerciseForm, self).full_clean()
