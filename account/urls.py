from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # registration
    path('register', views.register, name='register'),
    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification/<str:uidb64>/<str:token>', views.email_verification, name='email-verification'),
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
    
    # login/logout
    path('user-login', views.user_login, name='user-login'),
    path('user-logout', views.user_logout, name='user-logout'),
    
    # profile setting
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile-edit', views.profile_edit, name='profile-edit'),
    path('delete-account', views.delete_account, name='delete-account'),
    
    # password reset
    ## 1. submit email
    path("password-reset", auth_views.PasswordResetView.as_view(template_name="account/password/password_reset.html"), name="password_reset"),
    ## 2. password reset link sent successfully
    path('password-reset-sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_sent.html'), name='password_reset_done'),
    ## 3. confirm link sent to user email
    path('reset/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password_reset_form.html'), name='password_reset_confirm'),
    ## 4. reset password succesfully
    path('password-reset-success', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_success.html'), name='password_reset_complete'),
]
