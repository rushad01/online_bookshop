# Generated by Django 4.1 on 2022-11-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='author_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
