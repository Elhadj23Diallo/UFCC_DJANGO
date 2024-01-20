from django import forms
from django.contrib.auth import get_user_model

from . import models
import json


User = get_user_model()

class JSONField(forms.CharField):
    def to_python(self, value):
        if not value:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON')
    

class CommandeForm(forms.ModelForm):
    items = JSONField(label='items', required=False, widget=forms.HiddenInput(attrs={'id': 'items'}))
    transaction_id = forms.CharField(label='items', required=False, widget=forms.HiddenInput(attrs={'id': 'transaction_id'}))
    nom = forms.CharField(label='nom', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    prenom = forms.CharField(label='Prenom', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    adresse = forms.CharField(label='Adresse', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    pays = forms.CharField(label='Pays', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    telephone = forms.IntegerField(label='Telephone', widget=forms.NumberInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    code_postal = forms.CharField(label='Code Postal', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    total = forms.CharField(label='Somme Total à Payer', initial="GNF", widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_total', 'size':'50', 'style': 'background-color: black; color: white;'}))

    class Meta:
        model = models.Commande
        fields = ['items', 'transaction_id',  'total', 'nom', 'prenom','email', 'adresse', 'pays', 'telephone', 'code_postal']

class PhotoForm(forms.ModelForm):
    name = forms.CharField(label='name', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC;'}))
    caption = forms.TextInput()
    price = forms.DecimalField(label='price', widget=forms.NumberInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC;'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC;'}))
    telephone = forms.IntegerField(label='telephone', widget=forms.NumberInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC;'}))
    class Meta:
        model = models.Photo
        fields = ['name', 'image', 'caption', 'price', 'email', 'telephone']


class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ['name', 'title', 'content', 'price']
        
class CommentaireForm(forms.ModelForm):
    text = forms.CharField(label='text', widget=forms.TextInput(attrs={'size':'50', 'style': 'background-color: #FFFFCC; color: #336633;'}))
    parent_comment_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = models.Commentaire
        fields = ['text']  # Ajoutez d'autres champs si nécessaire

    def __init__(self, *args, **kwargs):
        super(CommentaireForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Commentaire'


#Modifier et supprimer Blog

class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ['name', 'title', 'content', 'price']
        
class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


#Modifier et supprimer Photo
class photoForm(forms.ModelForm):
    edit_photo = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Photo
        fields = ['name', 'caption', 'price', 'email', 'telephone']
        
 
class DeletePhotoForm(forms.Form):
    delete_photo = forms.BooleanField(widget=forms.HiddenInput, initial=True)

        
class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']