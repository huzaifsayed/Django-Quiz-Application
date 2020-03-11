from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, View, DeleteView

from apps.quiz.models import Question, QuizMakers, Answer, QuizTaker
from .forms import QuizHomeForm, QuizTakerForm

class HomeView(View):
    form_class = QuizHomeForm
    initial = {'key': 'value'}
    template_name = 'frontend/homepage.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        quessuccess = request.session.get('QuizSuccess', None)
        if quessuccess:
            return HttpResponseRedirect('/quiz')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            self.request.session['QuizMakerID'] = obj.id
            self.request.session['QuizMakerName'] = obj.quizmakername
            self.request.session['QuizMakerSlug'] = obj.slug
            self.request.session['QuizSuccess'] = False
            return HttpResponseRedirect('/quiz')

        return render(request, self.template_name, {'form': form})

class QuizDelete(View):

    def get(self, *args, **kwargs):
        self.request.session['QuizSuccess'] = False
        QuizMakers.objects.filter(id=self.kwargs['pk']).delete()
        return HttpResponseRedirect('/')

class QuizMaker(View):
    template_name = 'frontend/quizmaking.html'

    def get(self, request, *args, **kwargs):

        if not request.session.get('QuizMakerID', None):
            return HttpResponseRedirect('/')

        if request.session.get('QuizMakerID', None):
            
            quesresponse = request.GET.get('quesresponse', None)
            quesAttended = request.GET.get('quesAttended', None)
            quesChoice = request.GET.get('quesChoice', None)
            quesresponselast = request.GET.get('quesresponselast', None)

            print('----------------------------------------------------')
            print(quesresponse)
            print(quesAttended)
            print(quesChoice)
            print(quesresponselast)
            print('----------------------------------------------------')


            if quesresponselast:
                print(quesresponselast)
                self.request.session['QuizSuccess'] = True

            if quesresponse == 'True':
                
                ans = Answer.objects.create(question_id=quesAttended, answer=quesChoice, quizmaker_id=request.session.get('QuizMakerID'))
                
                data = {
                    'success': 'True'
                }
                return JsonResponse(data)
            else:
                questions = Question.objects.all()
                return render(request, self.template_name, {'questions': questions})
            
        else:
            return HttpResponseRedirect('/')

        

class QuizTakerView(View):
    template_name = 'frontend/quiztaker.html'

    def get(self, request, *args, **kwargs):
        print(self.kwargs['slug'])
        qm = QuizMakers.objects.get(slug=self.kwargs['slug'])
        quesans = Answer.objects.filter(quizmaker=qm).values_list('question', flat=True)
        questions = Question.objects.filter(id__in=quesans)
        answer = Answer.objects.filter(quizmaker=qm).values_list('answer', flat=True)

        quizscore = request.GET.get('quizscore', None)
        quiztakername = request.GET.get('quiztakername', None)

        if quizscore and quiztakername:
            self.request.session['QuizTaken'] = True
            qm = QuizMakers.objects.get(slug=self.kwargs['slug'])
            self.request.session['QuizSuccess'] = False
            QuizTaker.objects.create(quiz=qm, quiztakername=quiztakername, score=quizscore)
            scores = QuizTaker.objects.filter(quiz__slug=self.kwargs['slug']).values()
            del request.session['QuizMakerName1']
            data = {
                'success': 'True',
                'scores': list(scores)
            }
            return JsonResponse(data)

        aa = zip(questions, answer)

        return render(request, self.template_name, {'questions': aa})

class QuizTakerHomeView(View):
    form_class = QuizTakerForm
    initial = {'key': 'value'}
    template_name = 'frontend/homepagequizkater.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        scores = QuizTaker.objects.filter(quiz__slug=self.kwargs['slug'])
        self.request.session['QuizMakerName1'] = QuizMakers.objects.values_list('quizmakername', flat=True).get(slug=self.kwargs['slug'])
        return render(request, self.template_name, {'form': form, 'scores': scores})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            self.request.session['QuizTakerName'] = form.cleaned_data['quiztakername']
            self.request.session['QuizSlug'] = self.kwargs['slug']
            return HttpResponseRedirect('/quiz/'+self.kwargs['slug']+'/'+form.cleaned_data['quiztakername'])

        return render(request, self.template_name, {'form': form})