from django import forms
from apps.quiz.models import Question
from django.utils.translation import ugettext_lazy as _



class QuesCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['label', 'option1', 'option2','option3','option4',]
        labels = {
            "label": _("Question"),
        }