# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-01 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serwis', '0005_auto_20171201_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
