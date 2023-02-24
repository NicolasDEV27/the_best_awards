from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.all()
    context = render(request, "polls/index.html",{
        "latest_question_list": latest_question_list
    })
    return context


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = render(request, "polls/detail.html",{
        "question": question
    })
    return context
    

def results(request, question_id):
    return HttpResponse(f"You're seeing question number {question_id} results")
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    try:
       selected_choice = question.choice_set.get(pk= request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
      "question": question,
      "error_message": "You didn't choose an answer"
    })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

