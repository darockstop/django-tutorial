from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(req):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(req, 'polls/index.html', context)

def detail(req, q_id):
    q = get_object_or_404(Question, pk=q_id)
    return render(req, 'polls/detail.html', {'question': q})

def results(req, q_id):
    q = get_object_or_404(Question, pk=q_id)
    return render(req, 'polls/results.html', {'question': q})

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
    	selected.votes += 1
    	selected.save()
    	return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))