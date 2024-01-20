# Generated by Django 5.0 on 2023-12-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_photo_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='paiement_effectue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commande',
            name='paypal_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
