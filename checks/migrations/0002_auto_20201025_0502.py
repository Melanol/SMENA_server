# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-25 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]