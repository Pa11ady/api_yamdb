# Generated by Django 3.2.16 on 2024-06-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20240619_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, to='reviews.Genre', verbose_name='Slug жанра'),
        ),
    ]