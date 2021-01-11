from django.contrib import admin
from .models import *

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'rating', 'created')
    search_fields = ('title', 'creator')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'correct')

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'date', 'correct_answers')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(AnswerOption, AnswerOptionAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Like)
