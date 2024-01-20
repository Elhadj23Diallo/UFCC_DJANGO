from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
from django.contrib.auth import views as auth_views

import authentication.views

urlpatterns = [
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('profile-photo/upload', authentication.views.upload_profile_photo,
         name='upload_profile_photo'),
    path('confirmation/', authentication.views.confirmation, name='confirmation'),

]
