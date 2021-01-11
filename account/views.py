from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count

from .forms import UserForm, UserProfileForm, ChangePasswordForm, ChangeEmailForm
from quiz.models import Quiz, Result

from decimal import Decimal

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        all_q = Quiz.objects.filter(creator = request.user).order_by('title')
        flag = True if len(all_q) else False

        correct = Result.objects.filter(user=request.user).aggregate(corr=Sum('correct_answers'))['corr']
        all_ = Result.objects.filter(user=request.user).annotate(cnt=Count('quiz__question')).aggregate(all_=Sum('cnt'))['all_']

        if correct and all_:
            rating = Decimal(correct) / Decimal(all_) * 100
            rating = rating.quantize(Decimal("1.00")).normalize()
        else:
            rating = 0

        
        return render(request, 'account/profile.html', context={'flag':flag, 'rating':rating})

    def post(self, request):
        request.user.userprofile.picture = request.FILES.get('new_img')
        request.user.userprofile.save()
        context = {'success': 'Profile image was successfully changed!'}

        return render(request, 'account/profile.html', context)

@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        return render(request, 'account/change_password.html')

    def post(self, request):
        pwd_form = ChangePasswordForm(request.POST, request=request)
        user = request.user
        if pwd_form.is_valid():
            user.set_password(pwd_form.cleaned_data['new_password'])
            user.save()
            login(request, user)
            context = {'success': 'Your password was successfully changed!'}
            return render(request, 'account/profile.html', context)
        else:
            context = {'form': pwd_form}
            return render(request, 'account/change_password.html', context)

@method_decorator(login_required, name='dispatch')
class ChangeEmail(View):
    def get(self, request):
        return render(request, 'account/change_email.html')

    def post(self, request):
        email_form = ChangeEmailForm(request.POST, request=request)
        user = request.user
        if email_form.is_valid():
            user.email = email_form.cleaned_data['email']
            user.save()
            context = {'success': 'Your email was successfully changed!'}
            return render(request, 'account/profile.html', context)
        else:
            context = {'form': email_form}
            return render(request, 'account/change_email.html', context)

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quiz_list')
        else:
            return render(request, 'account/login.html', context={'errors':'User credentials are incorrect. Make sure that the user name and / or password are correct.'})
    else:
        return render(request, 'account/login.html')

def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'account/registration.html', context={'form':user_form})
    else:
        return render(request, 'account/registration.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('index')
