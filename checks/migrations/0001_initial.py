# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-20 21:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('k', 'kitchen'), ('c', 'client')], max_length=20)),
                ('order', django.contrib.postgres.fields.jsonb.JSONField()),
                ('status', models.CharField(choices=[('n', 'new'), ('r', 'rendered'), ('p', 'printed')], max_length=20)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('api_key', models.CharField(max_length=20, unique=True)),
                ('check_type', models.CharField(choices=[('k', 'kitchen'), ('c', 'client')], max_length=20)),
                ('point_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='printer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='checks.Printer'),
        ),
    ]
