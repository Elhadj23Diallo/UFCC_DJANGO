from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
import authentication.views
import blog.views


urlpatterns = [
    path('home/', blog.views.home, name='home'),
    path('boutique/', blog.views.boutique, name='boutique'),
    path('shop/', blog.views.shop, name='shop'),
    path('photo-feed/', blog.views.photo_feed, name='photo_feed'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('blog/create', blog.views.blog_and_photo_upload, name='blog_create'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('photo/<int:photo_id>', blog.views.view_photo, name='view_photo'),
    path('shop/<int:shop_id>', blog.views.view_shop, name='view_shop'),
    path('blog/<int:blog_id>/', blog.views.edit_blog, name='edit_blog'),
    path('photo/<int:photo_id>/', blog.views.edit_photo, name='edit_photo'),
    path('annulation/', blog.views.annulation, name='annulation'),
    path('photo/upload-multiple/', blog.views.create_multiple_photos,
         name='create_multiple_photos'),
    path('follow-users/', blog.views.follow_users, name='follow_users'),
    path('checkout/', blog.views.checkout, name='checkout'),
    path('commande/', blog.views.saisie_commande, name='saisie_commande'),
    path('commentaire-blog/<int:photo_id>/', blog.views.ajouter_commentaire, name='ajouter_commentaire'),
    path('load_photo/', blog.views.affiche_photo, name='load_photo'),
    path('checkout_p/<int:photo_id>/', blog.views.checkout_p, name='checkout_p'),
    path('payment_success/<int:photo_id>/', blog.views.payment_success, name='payment_success'),
    path('payment_failed/<int:photo_id>/', blog.views.payment_failed, name='payment_failed'),
    path('paypal-ipn/', blog.views.paypal_ipn, name='paypal-ipn')
]