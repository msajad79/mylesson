from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from core.settings import RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY
from .models import University, FieldStudy

class SignUpForm(UserCreationForm):
    university = forms.ModelChoiceField(queryset=University.objects.all())
    fieldstudy = forms.ModelChoiceField(queryset=FieldStudy.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    #captcha = ReCaptchaField(
    #    widget=ReCaptchaV2Checkbox()
    #)

