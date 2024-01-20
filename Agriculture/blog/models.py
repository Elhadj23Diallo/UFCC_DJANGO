from datetime import timezone
from django.conf import settings
from django.db import models
from PIL import Image
import os


class Photo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(verbose_name="images", upload_to="media/images/", null=True, blank=True)
    caption = models.CharField(max_length=128, blank=True, verbose_name='légende')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        if self.image:
            image_path = self.image.path
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            try:
                image = Image.open(image_path)
                image.thumbnail(self.IMAGE_MAX_SIZE)
                image.save(image_path)
            except Exception as e:
                print(f"Error resizing image: {e}")

""" def resize_image(self):
    if self.image:
        image_path = self.image.path
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        try:
            image = Image.open(image_path)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(image_path)
        except Exception as e:
            print(f"Error resizing image: {e}")"""
   
""" def resize_image(self):
    image = Image.open(self.image)
    image.thumbnail(self.IMAGE_MAX_SIZE)
    image.save(self.image.path)

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    self.resize_image()
         """
        
#model commentaire photo
class Commentaire(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)



    
""" class Shop(models.Model):
    nom = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(verbose_name='images', upload_to='media/images/', null=True, blank=True)
    description = models.CharField(max_length=128, blank=True, verbose_name='légende')
    date_created = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(CommentShop, related_name='products')

    def __str__(self):
        return self.nom """
    
class Shop(models.Model):
    nom = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(verbose_name="images", upload_to="media/images/", null=True, blank=True)
    caption = models.CharField(max_length=500, blank=True, verbose_name='légende')
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        if self.image:
            image_path = self.image.path
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            try:
                image = Image.open(image_path)
                image.thumbnail(self.IMAGE_MAX_SIZE)
                image.save(image_path)
            except Exception as e:
                print(f"Error resizing image: {e}")
    
    
class Blog(models.Model):
    name = models.CharField(max_length=100, blank=True)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128, verbose_name='titre')
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    content = models.CharField(max_length=5000, verbose_name='contenu')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(null=True)

    def _get_word_count(self):
        return len(self.content.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)


class BlogContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)
    starrede = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('contributor', 'blog')

class Commande(models.Model):
    items = models.CharField(max_length=300)
    nom = models.CharField(max_length=200)
    total = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    adresse = models.CharField(max_length=200)
    pays = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    quartier = models.CharField(max_length=200)
    telephone = models.IntegerField()
    code_postal = models.IntegerField()
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return self.nom
        
   
        
""" 
class Commande(models.Model):
    items = models.CharField(max_length=300)
    nom = models.CharField(max_length=200)
    total = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    quartier = models.CharField(max_length=200)
    pays = models.CharField(max_length=200)
    telephone = models.IntegerField()
    code_postal = models.IntegerField()
    date_commande = models.DateTimeField(auto_now=True)
    
    # Nouveaux champs pour PayPal
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    paiement_effectue = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_commande']

    def __str__(self):
        return self.nom """