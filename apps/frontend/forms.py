from django import forms
from apps.quiz.models import QuizMakers, QuizTaker
from django.utils.translation import ugettext_lazy as _


class QuizHomeForm(forms.ModelForm):

    class Meta:
        model = QuizMakers
        fields = ['quizmakername', ]
        labels = {
            "quizmakername": _(""),
        }
        help_texts = {'quizmakername': "Enter You Name !!!",}

class QuizTakerForm(forms.ModelForm):

    class Meta:
        model = QuizTaker
        fields = ['quiztakername', ]
        labels = {
            "quiztakername": _(""),
        }
        help_texts = {'quiztakername': "Enter You Name !!!",}