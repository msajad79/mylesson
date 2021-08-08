from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns = [
    
    path('profile/', views.profile, name='profile'),

    path('login/', views.LoginView.as_view(), name='login'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'),
    
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/activate/<uidb64>/<token>/', views.ActiveAccountView.as_view(), name='activate_account'),
]
