# Generated by Django 5.2.4 on 2025-07-14 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kayakutils', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='county',
            options={'verbose_name_plural': 'Counties'},
        ),
    ]
