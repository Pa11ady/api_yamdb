# Generated by Django 3.2 on 2024-06-26 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_alter_title_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('year',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]