from django.urls import path
from .views import *

urlpatterns = [
    path('about/', get_about_page, name = 'about'),
    path('faq/', get_faq_page, name = 'faq'),
    path('add_quiz/', AddQuiz.as_view(), name = 'add_quiz'),
    path('list/', get_quizzes, name = 'quiz_list'),
    path('search/', search_quiz, name = 'search'),
    path('quiz_page/<int:id>', get_quiz_prew, name = 'quiz_page'),
    path('play/<int:id>', get_question, name = 'play'),
    path('like/', like_quiz, name = 'like'),
    path('get_next_page/', get_next_page, name = 'get_next_page'),
    path('check_answer/<int:id>', check_answer, name = 'check_answer'),
    path('quiz_result/<int:id>', get_quiz_result, name = 'quiz_result'),
    path('results/<str:username>', get_results, name = 'results'),
    
]
