# Generated by Django 5.2.4 on 2025-07-12 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayakutils', '0001_initial'),
        ('launchinfo', '0013_delete_city_delete_country_delete_county_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.city'),
        ),
        migrations.AlterField(
            model_name='launch',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.country'),
        ),
        migrations.AlterField(
            model_name='launch',
            name='county',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.county'),
        ),
        migrations.AlterField(
            model_name='launch',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.state'),
        ),
    ]
