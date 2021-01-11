from django import template
from django.db.models import Count, Q

from quiz.models import Question, Quiz, Like
from django.core.paginator import Paginator

register = template.Library()

@register.filter(name='likes')
def likes(value):
    return Quiz.objects.annotate(cnt=Count('like', filter=Q(like__liked=True))).get(id=value.id).cnt

@register.simple_tag
def is_liked(quiz, user):
    like = Like.objects.get_or_create(user=user, quiz=quiz)[0]
    return "liked" if like.liked else ""

@register.inclusion_tag('quiz/question.html')
def get_question_data(request):
    curr = request.session['current']
    question = Question.objects.get(id=request.session['q_order'][curr])

    return {'question': question}

@register.inclusion_tag('quiz/popular_block.html')
def get_popular_block(request, profile=None):
    user = request.user
    qall = Quiz.objects.all()
    if profile:
        popular_quizes = qall.filter(creator = user).annotate(cnt=Count('like', filter=Q(like__liked=True))).order_by('-cnt')[:4]
    else:
        popular_quizes = qall.annotate(cnt=Count('like', filter=Q(like__liked=True))).order_by('-cnt')[:4]

    return {'popular_q': popular_quizes, 'request':request}

@register.inclusion_tag('quiz/all_block.html')
def get_all_block(request, profile=None):
    user = request.user
    if profile:
        all_quizes = Quiz.objects.filter(creator = user).order_by('title')
    else:
        all_quizes = Quiz.objects.all().order_by('title')

    p = Paginator(all_quizes, 15)
    page = p.page(1)

    return {'all_q': page, 'request': request}
