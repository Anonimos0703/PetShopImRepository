# Generated by Django 5.1.1 on 2024-12-01 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0001_initial'),
        ('users', '0002_productrating_comment_alter_productrating_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='admin_page.product'),
        ),
    ]
