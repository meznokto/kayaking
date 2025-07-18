# Generated by Django 5.2.4 on 2025-07-12 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayakutils', '0001_initial'),
        ('launchinfo', '0011_city_county_city_state_county_state_state_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='county',
        ),
        migrations.RemoveField(
            model_name='city',
            name='state',
        ),
        migrations.AlterField(
            model_name='launch',
            name='city',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.city'),
        ),
        migrations.RemoveField(
            model_name='state',
            name='country',
        ),
        migrations.AlterField(
            model_name='launch',
            name='country',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.country'),
        ),
        migrations.RemoveField(
            model_name='county',
            name='state',
        ),
        migrations.AlterField(
            model_name='launch',
            name='county',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.county'),
        ),
        migrations.AlterField(
            model_name='launch',
            name='state',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kayakutils.state'),
        ),
    ]
