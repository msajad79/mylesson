from core.settings import EMAIL_NAME
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import LoginForm, SignUpForm
from .tokens import account_activation_token


@login_required()
def profile(request):
    return HttpResponse('profile')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login/login.html', context={'form':form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        context = {}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if not user is None:
                login(request, user)
                context['message'] = 'You are logged in.'
                return redirect('profile')
            context['message'] = 'username or password is invalid'
        context['form'] = form
        return render(request, 'accounts/login/login.html', context=context)

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup/signup.html', context={'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user:User = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.profile.university = form.cleaned_data.get('university')
            user.profile.fieldstudy = form.cleaned_data.get('fieldstudy')
            user.save()
            current_site = get_current_site(request)
            subject = 'Email Confirm'
            email_template = 'accounts/signup/email_template.html'
            context_email = {
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
            message = render_to_string(email_template, context_email)
            try:
                send_mail(subject, message, EMAIL_NAME, [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('invalid header found.')
            return render(request, 'accounts/signup/confirm_email.html')
            
        form = SignUpForm()
        return render(request, 'accounts/signup/signup.html', context={'form':form})

class ActiveAccountView(View):
	def get(self, request, uidb64, token):
		user = get_object_or_404(User ,id=urlsafe_base64_decode(uidb64).decode())
		if account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			return render(request, 'accounts/signup/confirm_email_done.html')
		return Http404()

class PasswordResetView(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="accounts/password/password_reset.html", context={"password_reset_form":password_reset_form})

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                current_site = get_current_site(request)
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password/email_template.html"
                    context_email = {
                        'domain':current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    }
                    message = render_to_string(email_template_name, context_email)
                    try:
                        send_mail(subject, message, EMAIL_NAME, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")

        return render(request, 'accounts/password/password_reset.html', context={'password_reset_form':password_reset_form})


