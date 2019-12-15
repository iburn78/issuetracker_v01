from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Choice, Question
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView

def index(request): 
    latest_question_list = Question.objects.all().order_by('-pub_date') #[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'polls/index.html', context)

def detail(request, question_id): 
    question = get_object_or_404(Question, pk=question_id)
    request.session['Current_question_id'] = question_id
    
    return render(request, 'polls/detail.html', {'question':question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question, 
            'error_message': "You didn't select a choice",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, 'polls/results.html', {'question':question})


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text']

    def form_valid(self, form):
        # print("This prints when called ---")
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = "/polls/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

class ChoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # print("On startup, this sentence is executed.")
    model = Choice 
    fields = ['choice_text']
    # template_name = "polls/choice_form.html"
    
    def get(self, request, *args, **kwargs):
        # print("GET Function Called")
        self.object = None
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['question_obj'] = Question.objects.get(id= self.request.session['Current_question_id']) # Question.objects.get(id=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):  # https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/#the-save-method 
        choice = form.save(commit=False)
        choice.question = Question.objects.get(id= self.request.session['Current_question_id']) 
        choice.save()
        form.save_m2m()
        self.object = choice
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        # choice = self.get_object()
        if self.request.user == Question.objects.get(id = self.request.session['Current_question_id']).author: 
            return True
        return False
    
