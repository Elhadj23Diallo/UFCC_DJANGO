# Generated by Django 5.0 on 2023-12-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_commande_blog_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcontributor',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogcontributor',
            name='starrede',
            field=models.BooleanField(default=False),
        ),
    ]