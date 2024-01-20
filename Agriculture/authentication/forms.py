from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={'class':'form-control champe-bordure', 'placeholder':"Nom d'utilisateur"}), label="Nom d'utilisateur")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control champe-bordure', 'placeholder':'Mot de passe'}), label="Mot de passe") 

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={'class':'form-control champ-bordure', 'placeholder':"Nom d'utilisateur"}), label="Nom d'utilisateur")
    email = forms.EmailField(max_length=63, widget=forms.EmailInput(attrs={'class':'form-control champ-bordure', 'placeholder':'Adresse e-mail'}), label="Adresse e-mail")
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control champ-bordure', 'placeholder':'Prénom'}), label="Prénom")
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control champ-bordure', 'placeholder':'Nom'}), label="Nom")
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control champ-bordure', 'placeholder':'Mot de passe'}), label="Mot de passe")
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control champ-bordure', 'placeholder':'Confirmation du mot de passe'}), label="Confirmation du mot de passe")
    class Meta(UserCreationForm):
        model=get_user_model()
        fields=['username', 'email', 'first_name', 'last_name', 'role']


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo', )
