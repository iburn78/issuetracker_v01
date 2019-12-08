from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self): 
        return self.question_text

    def get_absolute_url(self): 
        return reverse('polls:index')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self): 
        return self.choice_text

    def get_absolute_url(self): 
        return reverse('polls:index')

