# Generated by Django 5.2.4 on 2025-07-12 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_kayakuser_picture_kayakuser_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kayakuser',
            old_name='thumbnail',
            new_name='avatar',
        ),
    ]
