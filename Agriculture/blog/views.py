from itertools import chain

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models

from django.conf import settings
import uuid
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from paypal.standard.forms import PayPalPaymentsForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from decouple import config  # Importez la fonction config si nécessaire

def checkout_p(request, photo_id):
    shop = get_object_or_404(models.Shop, id=photo_id)
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_CLIENT_ID,
        'amount': shop.price,
        'item_name': shop.nom,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment_success', kwargs={'photo_id': photo_id})}",
        'cancel_url': f"http://{host}{reverse('payment_failed', kwargs={'photo_id': photo_id})}",
    }
    
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'shop': shop,
        'paypal': paypal_payment
    }
    return render(request, 'blog/checkout_p.html', context)

@csrf_exempt
def payment_success(request, photo_id):
    blog = models.Shop.objects.get(id=photo_id)
    return render(request, 'blog/payment_success.html', {'blog':blog})

@csrf_exempt
def payment_failed(request, photo_id):
    blog = models.Shop.objects.get(id=photo_id)
    return render(request, 'blog/payment_failed.html', {'blog':blog})

# blog/views.py
from django.http import HttpResponse

def paypal_ipn(request):
    # Cette vue peut être vide ou renvoyer une réponse générique
    return HttpResponse("PayPal IPN endpoint reached.")


@login_required
@permission_required('blog.add_photo')
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})



@login_required
def home(request):
    search_term = request.GET.get('search', '')
        # Recherche dans le modèle Blog
    blogs = models.Blog.objects.filter(
            Q(name__icontains=search_term) |
            Q(contributors__in=request.user.follows.all()) |
            Q(starred=True)
        )

        # Recherche dans le modèle Photo
    photos = models.Photo.objects.filter(name__icontains=search_term, uploader__in=request.user.follows.all()).exclude(
            blog__in=blogs
        )

    blogs_and_photos = sorted(
            chain(blogs, photos),
            key=lambda instance: instance.date_created,
            reverse=True
        )

    paginator = Paginator(blogs_and_photos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_term': search_term}

    return render(request, 'blog/home.html', context)


#vue pour la boutique
@login_required
def boutique(request):
    search_term = request.GET.get('search', '')
        # Recherche dans le modèle Blog
    blogs = models.Blog.objects.filter(
            Q(name__icontains=search_term) |
            Q(contributors__in=request.user.follows.all()) |
            Q(starred=True)
        )

        # Recherche dans le modèle Photo
    photos = models.Photo.objects.filter(name__icontains=search_term, uploader__in=request.user.follows.all()).exclude(
            blog__in=blogs
        )

    blogs_and_photos = sorted(
            chain(blogs, photos),
            key=lambda instance: instance.date_created,
            reverse=True
        )

    paginator = Paginator(blogs_and_photos, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_term': search_term}

    return render(request, 'blog/boutique.html', context)

@login_required
def affiche_photo(request):
    search_term = request.GET.get('search', '')
    paginator = models.Blog.filter(name__icontains=search_term)
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) | Q(starred=True))
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()).exclude(
        blog__in=blogs)

    blogs_and_photos = sorted(
        chain(blogs, photos),
        key=lambda instance: instance.date_created,
        reverse=True
    )
    paginator = Paginator(blogs_and_photos, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search_term':search_term}

    return render(request, 'blog/load_photo.html', context=context)


@login_required
@permission_required(['blog.add_photo', 'blog.add_blog'])
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('home')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/create_blog_post.html', context=context)

@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})

def view_photo(request, photo_id):
    photo = get_object_or_404(models.Photo, id=photo_id)
    return render(request, 'blog/view_photo.html', {'photo': photo})

def view_shop(request, shop_id):
    shop = get_object_or_404(models.Shop, id=shop_id)
    return render(request, 'blog/view_shop.html', {'shop': shop})

#Modifier et Supprimer photo
@login_required
@permission_required('blog.change_blog')
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', context=context)


#Modifier et Supprimer photo
@login_required
@permission_required('blog.change_blog')
def edit_photo(request, photo_id):
    photo = get_object_or_404(models.Photo, id=photo_id)
    edit_form = forms.PhotoForm(instance=photo)
    delete_form = forms.DeletePhotoForm()
    if request.method == 'POST':
        if 'edit_photo' in request.POST:
            edit_form = forms.PhotoForm(request.POST, instance=photo)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_photo' in request.POST:
            delete_form = forms.DeletePhotoForm(request.POST)
            if delete_form.is_valid():
                photo.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_photo.html', context=context)



@login_required
@permission_required('blog.add_photo')
def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST':
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
    return render(request, 'blog/create_multiple_photos.html', {'formset': formset})


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html', context={'form': form})

 
 
def photo_feed(request):
    search_term = request.GET.get('search', '')
    photos = models.Photo.objects.filter(name__icontains=search_term, uploader__in=request.user.follows.all()).order_by('-date_created')

    paginator = Paginator(photos, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'search_term': search_term}
    return render(request, 'blog/photo_feed.html', context=context)

""" def photo_feed(request):
    search_term = request.GET.get('search', '')
    paginator = models.Photo.objects.filter(name__icontains=search_term)
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()).order_by('-date_created')
    paginator = Paginator(photos, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'search_term':search_term}
    return render(request, 'blog/photo_feed.html', context=context) """

def saisie_commande(request):
    if request.method == 'POST':
        form = forms.CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = forms.CommandeForm()
    context = {'form': form}
    return render(request, 'blog/commande.html', context)

import json

def checkout(request):
    host = request.get_host()
    paypal_payment = None

    if request.method == 'POST':
        form = forms.CommandeForm(request.POST)
        if form.is_valid():
            # Sauvegarder la commande
            commande = form.save(commit=False)

            # Convertir la chaîne JSON en objet Python
            items = form.cleaned_data['items']
            commande.items = items

            commande = form.save()

            # Préparer les données pour PayPal
            paypal_checkout = {
                'business': 'isaacdiallo30@gmail.com',
                'amount': commande.total,
                'item_name': commande.items,
                'invoice': commande.total,
                'currency_code': 'USD',
                'notify_url': f"http://{host}{reverse('paypal-ipn')}",
                'return_url': f"http://{host}{reverse('confirmation')}",
                'cancel_url': f"http://{host}{reverse('annulation')}",
            }

            # Initialiser le formulaire PayPalPaymentsForm
            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

            return redirect('confirmation')
    else:
        form = forms.CommandeForm()

    context = {
        'form': form,
        'paypal': paypal_payment
    }

    return render(request, 'blog/checkout.html', context)

def annulation(request):
    return render(request, 'blog/annulation.html')

@login_required
def ajouter_commentaire(request, photo_id):
    photo = get_object_or_404(models.Photo, pk=photo_id)

    if request.method == 'POST':
        form = forms.CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.uploader = request.user
            commentaire.photo = photo
            commentaire.save()

            # Si le commentaire est une réponse à un commentaire existant
            parent_comment_id = form.cleaned_data.get('parent_comment_id')
            if parent_comment_id:
                parent_comment = models.Commentaire.objects.get(pk=parent_comment_id)
                commentaire.parent_comment = parent_comment
                commentaire.save()

            return redirect('ajouter_commentaire', photo_id=photo.id)
    else:
        form = forms.CommentaireForm()

    return render(request, 'blog/commentaire_blog.html', {'form': form, 'photo': photo, 'commentaires': photo.commentaire_set.all()})



#Vue pour la boutique en ligne
def shop(request):
    search_term = request.GET.get('search', '')
    photos = models.Shop.objects.filter(nom__icontains=search_term)
    paginator = Paginator(photos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'search_term':search_term
    }
    return render(request, 'blog/shop.html', context)


# views.py
from django.http import JsonResponse

def get_paypal_keys(request):
    paypal_keys = {
        'sandbox_client_id': 'Af84vG-dNyVafwVXDCWXPrfGEWRcj6Wzp996ctIZD3gyD4Ohl-yEkh3d8lu4sbPDaoa_NhzQqxoRqWFg',
        'production_client_id': 'votre_production_client_id'
        # Ajoutez d'autres clés si nécessaire
    }
    return JsonResponse(paypal_keys)

# views.py (exemple)
from django.http import JsonResponse

def get_paypal_keys(request):
    # Logique pour récupérer les clés depuis votre système sécurisé
    paypal_keys = {
        'sandboxKey': 'Af84vG-dNyVafwVXDCWXPrfGEWRcj6Wzp996ctIZD3gyD4Ohl-yEkh3d8lu4sbPDaoa_NhzQqxoRqWFg',
        #'productionKey': 'Votre clé de production',
    }

    return JsonResponse(paypal_keys)
