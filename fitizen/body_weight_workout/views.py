from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from .models import BodyWeightWorkout, WeightExercise
from .forms import WeightExerciseForm

from braces import views


# Create your views here.
class CreateWorkout(
    views.LoginRequiredMixin,
    views.MessageMixin,
    View
):

    def set_exercises(self, workout):
        pullup = WeightExercise(exercise='PL', workout=workout)
        dip = WeightExercise(exercise='D', workout=workout)
        squat = WeightExercise(exercise='SQ', workout=workout)
        lsit = WeightExercise(exercise='LS', workout=workout)
        pushup = WeightExercise(exercise='PU', workout=workout)
        row = WeightExercise(exercise='RW', workout=workout)
        pullup.save()
        dip.save()
        squat.save()
        lsit.save()
        pushup.save()
        row.save()

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        recent_workout = BodyWeightWorkout.objects.filter(user=request.user.id).datetimes('created', 'day', order='DESC')[:1]
        if len(recent_workout) > 0:
            recent_workout = list(recent_workout)
            difference = (now - recent_workout[0])
            if difference.days == 0:
                self.messages.success("You already worked out today, take a break!")
                return redirect('home')
        else:
            user = request.user
            workout = BodyWeightWorkout(user=user)
            workout.save()
            self.set_exercises(workout)
            self.messages.success("New workout created!")
            return redirect('home')


class WorkoutView(
    views.LoginRequiredMixin,
    views.MessageMixin,
    TemplateView
):

    template_name = 'workout.html'

    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        if request.user.username == username:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect('home')

    def get_context_data(self, **kwargs):
        context = super(WorkoutView, self).get_context_data(**kwargs)
        workout_id = int(self.kwargs['workout_id'])
        context['workout_id'] = str(workout_id)
        context['pullups'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='PL'))[0]
        context['dips'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='D'))[0]
        context['squats'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='SQ'))[0]
        context['lsits'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='LS'))[0]
        context['pushups'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='PU'))[0]
        context['rows'] = list(WeightExercise.objects.filter(workout_id=workout_id, exercise='RW'))[0]
        return context


class UpdateWorkout(
    views.LoginRequiredMixin,
    views.MessageMixin,
    View
):

    def set_choices(self, group_number):

        EXERCISE_CHOICES = {
                1: [
                    (('1', 'Level 1: Wall Pushup'),
                     ('2', 'Level 2: Incline Pushup'),
                     ('3', 'Level 3: Pushup'),
                     ('4', 'Level 4: Diamond Pushup')),
                    (('1', 'Level 1: Vertical Row'),
                     ('2', 'Level 2: Incline Row'),
                     ('3', 'Level 3: Row'))],
                2: [
                    (('1', 'Level 1: Wall Pushup'),
                     ('2', 'Level 2: Incline Pushup'),
                     ('3', 'Level 3: Pushup'),
                     ('4', 'Level 4: Diamond Pushup')),
                    (('1', 'Level 1: Vertical Row'),
                     ('2', 'Level 2: Incline Row'),
                     ('3', 'Level 3: Row'))],
                3: [
                    (('1', 'Level 1: Wall Pushup'),
                     ('2', 'Level 2: Incline Pushup'),
                     ('3', 'Level 3: Pushup'),
                     ('4', 'Level 4: Diamond Pushup')),
                    (('1', 'Level 1: Vertical Row'),
                     ('2', 'Level 2: Incline Row'),
                     ('3', 'Level 3: Row'))]
        }
        return EXERCISE_CHOICES[group_number]

    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        if request.user.username == username:
            templates = {1: 'update_group1.html', 2: 'update_group2.html',
                         3: 'update_group3.html'}
            workout_id = self.kwargs['workout_id']
            group = self.kwargs['group']
            choices = self.set_choices(int(group))
            template = templates[int(group)]
            form1 = WeightExerciseForm(view_choices=choices[0],
                                       prefix='ex1')
            form2 = WeightExerciseForm(view_choices=choices[1],
                                       prefix='ex2')
            return render(request, template, {
                          'form1': form1,
                          'form2': form2,
                          'workout_id': workout_id,
                          'group': group,
                          })
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        group = self.kwargs['group']
        choices = self.set_choices(int(group))
        form1 = WeightExerciseForm(view_choices=choices[0], data=request.POST, prefix='ex1')
        form2 = WeightExerciseForm(view_choices=choices[1], data=request.POST, prefix='ex2')
        groups = {1: ('PL', 'D'), 2: ('SQ', 'LS'), 3: ('PU', 'RW')}
        if form1.is_valid() and form2.is_valid():
            workout_id = int(self.kwargs['workout_id'])
            group_number = int(self.kwargs['group'])
            w1 = WeightExercise.objects.get(workout=workout_id, exercise=groups[group_number][0])
            w2 = WeightExercise.objects.get(workout=workout_id, exercise=groups[group_number][1])
            f1 = WeightExerciseForm(view_choices=choices[0], data=request.POST, instance=w1, prefix='ex1')
            f2 = WeightExerciseForm(view_choices=choices[1], data=request.POST, instance=w2, prefix='ex2')
            f1.save()
            f2.save()
            return HttpResponseRedirect('/' + request.user.username + '/workout/' + str(workout_id))
        else:
            workout_id = self.kwargs['workout_id']
            group = self.kwargs['group']
            print request.POST
            self.messages.success("Invalid!")
            return HttpResponseRedirect('/' + request.user.username + '/update_workout/' + str(workout_id) + '/' + str(group))
