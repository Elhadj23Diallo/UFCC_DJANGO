from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .import models

from . import forms


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})


def logout_page(request):
     logout(request)
     return redirect('login')    

@login_required
def confirmation(request):
    # Supposons que vous ayez une logique pour déterminer la commande et l'utilisateur associé ici
    # Dans cet exemple, je suppose que vous avez un utilisateur connecté
    utilisateur_commande = models.User.objects.get(username=request.user.username)

    return render(request, 'blog/confirmation.html', {'utilisateur_commande': utilisateur_commande})
