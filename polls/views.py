from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# Notes
#
# __lte means less than or equal, there is also also lt, gte, and gt
# where does get_queryset get called?


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question 
    template_name = 'polls/detail.html'
    # context_object_name = 'question' is the default

    def get_queryset(self):
        """Exclude unpublished questions."""
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Exclude unpublished questions."""
        return Question.objects.filter(pub_date__lte=timezone.now())



def vote(req, q_id):
    q = get_object_or_404(Question, pk=q_id)
    try:
    	selected = q.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
    	# redisplay form
    	return render(req, 'polls/detail.html', {
    		'qusetion': q, 
    		'error_message': 'Error. Please select a choice.',
    		})
    else:
    	selected.votes += 1 # this is a race condition
    	selected.save()
    	return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))
