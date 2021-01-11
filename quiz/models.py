from django.db import models
from django.contrib.auth.models import User

import os

# Create your models here.

def generate_quiz_filename(instance, filename):
    return 'quiz_images/quiz_{0}/{1}'.format(instance.id, filename)

class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_quiz_filename, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Quiz {}".format(self.title)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self):
        tmp = '+' if self.liked else '-'
        return "User: {0}, Quiz_id: {1}, Liked: {2}".format(self.user, self.quiz.id, tmp)

class Question(models.Model):
    text = models.CharField(max_length=255)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return 'Answer obj for "{}"'.format(self.question)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    correct_answers = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{0} result from {1}".format(self.user.username, self.date)
