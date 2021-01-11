from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError("The passwords you entered don't match. Please, re-enter your passwords.")
        return self.cleaned_data['password2']

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_old_password(self):
        if self.request:
            if self.request.user.check_password(self.cleaned_data['old_password']):
                return self.cleaned_data['old_password']
            else:
                raise ValidationError("Your current password is wrong.")
        else:
            raise ValidationError("You can not change password this time. Please, try later or inform the site administration.")

    def clean_new_password2(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['new_password2']:
            raise ValidationError("The passwords you entered don't match. Please, re-enter your passwords.")
        return self.cleaned_data['new_password']

class ChangeEmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        if self.request:
            if self.request.user.check_password(self.cleaned_data['password']):
                return self.cleaned_data['password']
            else:
                raise ValidationError("Your current password is wrong.")
        else:
            raise ValidationError("You can not change password this time. Please, try later or inform the site administration.")

    class Meta:
        model = User
        fields = ('email', 'password')
