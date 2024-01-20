from django.contrib import admin
from .import models

# Register your models here.
class AdminBlog(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(models.Blog, AdminBlog)



class AdminCommande(admin.ModelAdmin):
    list_display = ('items_display', 'nom', 'prenom', 'telephone', 'email', 'adresse', 'pays', 'total', 'date_commande',)

    def items_display(self, obj):
        # Mettez ici le code pour formater l'affichage du champ items
        return obj.items  # Exemple basique, ajustez selon vos besoins

    items_display.short_description = 'items'  # Nom de l'en-tête dans l'interface admin
admin.site.register(models.Commande, AdminCommande)
    

admin.site.register(models.Photo)

admin.site.register(models.Shop)