# Generated by Django 5.2.4 on 2025-07-14 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('launchinfo', '0019_alter_launch_bathroom_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch',
            name='bathroom_type',
            field=models.SmallIntegerField(choices=[(0, 'None'), (1, 'Outhouse'), (2, 'Plumbed'), (3, 'Nearby')], default=0),
        ),
    ]
