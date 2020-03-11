from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import unique_slug_generator


class Question(models.Model):
    label = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000, null = True, blank = True)
    option4 = models.CharField(max_length=1000, null = True, blank = True)
    def __str__(self):
        return self.label

class QuizMakers(models.Model):
    quizmakername = models.CharField(max_length=1000)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    quizques = models.ManyToManyField(Question, blank=True)
    def __str__(self):
        return self.quizmakername

def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 

pre_save.connect(pre_save_receiver, sender = QuizMakers) 


class QuizTaker(models.Model):
    quiz = models.ForeignKey(QuizMakers, on_delete=models.CASCADE)
    quiztakername = models.CharField(max_length=1000)
    score = models.IntegerField(default=0)
    def __str__(self):
        return self.quiztakername

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    quizmaker = models.ForeignKey(QuizMakers, on_delete=models.CASCADE)
    def __str__(self):
        return self.answer