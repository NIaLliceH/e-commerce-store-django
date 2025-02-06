from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('email-verification/<str:uidb64>/<str:token>', views.email_verification, name='email-verification'),
    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
    
    path('user-login', views.user_login, name='user-login'),
    path('user-logout', views.user_logout, name='user-logout'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile-setting', views.profile_setting, name='profile-setting'),
    path('delete-account', views.delete_account, name='delete-account')
]
