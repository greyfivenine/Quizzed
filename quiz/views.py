from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

import json
from decimal import Decimal

from .models import *

# Create your views here.

def get_about_page(request):
    return render(request, 'quiz/about.html')

def get_faq_page(request):
    return render(request, 'quiz/faq.html')

@login_required
def search_quiz(request):
    if request.method == "GET":
        query = request.GET["query"]
        if query.strip() == '':
            all_quizes = Quiz.objects.filter(title__contains=query)
            p = Paginator(all_quizes, 15)
            result = p.page(1)
        else:
            result = Quiz.objects.filter(title__contains=query)
        context = {'all_q': result}
        return render(request, 'quiz/all_block.html', context=context)

@login_required
def get_next_page(request):
    if request.method == "GET":
        all_quizes = Quiz.objects.all().order_by('title')
        p = Paginator(all_quizes, 15)
        next = int(request.GET['next'])
        if next > p.num_pages:
            return HttpResponse(False)
        else:
            page = p.page(next)
            context = {'all_q': page}
            return render(request, 'quiz/all_block.html', context=context)

@login_required
def get_results(request, username):
    if username != request.user.username:
        return render(request, 'quiz/forbidden.html')
    else:
        results = Result.objects.filter(user__username = username)
        context = {'username': username, 'results': results}
        return render(request, 'quiz/results.html', context=context)

@login_required
def like_quiz(request):
    likes = 0
    if request.method == "GET":
        id = request.GET.get("id", 1)
        like = Like.objects.get_or_create(quiz = Quiz.objects.get(id = id), user = request.user)[0]
        like.liked = not like.liked
        like.save()
        return HttpResponse(like.liked)

@login_required
def get_quiz_result(request, id):
    quiz_result = Result.objects.get(id=id)
    context = {'result': quiz_result}
    return render(request, 'quiz/quiz_result.html', context=context)

@login_required
def get_quizzes(request):
    return render(request, 'quiz/quiz_list.html')

@login_required
def get_quiz_prew(request, id):
    quiz = Quiz.objects.get(id=id)
    context = {
        'quiz':quiz
    }
    request.session['q_order'] = [q.id for q in Quiz.objects.get(id=id).question_set.all()]
    request.session['current'] = 0
    return render(request, 'quiz/quiz.html', context=context)

@login_required
def get_question(request, id):
    return render(request, 'quiz/quiz_answer.html')

@login_required
def check_answer(request, id):
    answ = AnswerOption.objects.get(id=id)
    if not request.session.get('correct', False):
        request.session['correct'] = 0

    if answ.correct:
        request.session['correct'] += 1

    request.session['current'] += 1

    if request.session['current'] == len(request.session['q_order']):
        r = Result(user = request.user, quiz = answ.question.quiz)
        r.correct_answers = request.session['correct']
        r.save()
        del request.session['q_order']
        del request.session['current']
        del request.session['correct']
        return redirect('quiz_result', id=r.id)
    else:
        return redirect('play', id=answ.question.quiz.id)

@method_decorator(login_required, name='dispatch')
class AddQuiz(View):
    def get(self, request):
        return render(request, 'quiz/quiz_add.html')

    def post(self, request):
        data = json.loads(request.POST['json_data'])
        quiz_obj = Quiz(creator = request.user, title = data.get('quiz_title'), description = data.get('quiz_description'))
        quiz_obj.save(commit=False)
        quiz_obj.image = request.FILES.get('quiz_logo')
        quiz_obj.save()
        for q in data.get('questions'):
            quest_obj = Question(text = q.get('question'), quiz = quiz_obj)
            quest_obj.save()

            for ind, answ in enumerate(q.get('answers')):
                answ_obj = Answer.objects.get_or_create(text = answ)[0]

                answ_opt_obj = AnswerOption(question = quest_obj, answer = answ_obj)

                if ind in q.get('correct'):
                    answ_opt_obj.correct = True

                answ_opt_obj.save()

        return render(request, 'quiz/quiz_add.html')
