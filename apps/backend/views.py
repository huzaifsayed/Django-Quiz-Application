from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.quiz.models import Question, QuizMakers, QuizTaker

from .forms import QuesCreateForm

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'backend/dashboard.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['question_count'] = Question.objects.all().count()
        context['quismaker_count'] = QuizMakers.objects.all().count()
        context['quiztaker_count'] = QuizTaker.objects.all().count()
        return context

class QuestionsDisplay(LoginRequiredMixin, ListView):
    template_name = 'backend/questions.html'
    model = Question
    context_object_name = 'questions'

class QuestionsCreate(LoginRequiredMixin, CreateView):
    template_name = 'backend/questioncreate.html'
    model = Question
    form_class = QuesCreateForm
    success_url = '/questions'

    # def form_valid(self, form):
    #     obj = form.save()
                
    #     label = form.cleaned_data['label']
    #     option1 = form.cleaned_data['option1']
    #     option2 = form.cleaned_data['option2']
    #     option3 = form.cleaned_data['option3']
    #     option4 = form.cleaned_data['option4']

    #     if option1:
    #         obj.option.create(text=option1)
    #     if option2:
    #         obj.option.create(text=option2)
    #     if option3:
    #         obj.option.create(text=option3)
    #     if option4:
    #         obj.option.create(text=option4)
    
    #     return super(QuestionsCreate, self).form_valid(form)

class QuestionsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'backend/questiondelete.html'
    model = Question
    success_url = '/questions'
