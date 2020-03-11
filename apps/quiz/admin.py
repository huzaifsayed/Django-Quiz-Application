from django.contrib import admin
from .models import Question, QuizMakers, QuizTaker, Answer

admin.site.register(Question)
admin.site.register(QuizMakers)
admin.site.register(QuizTaker)
admin.site.register(Answer)
