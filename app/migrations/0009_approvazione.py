# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-26 16:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_auto_20180826_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approvazione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alunno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('corso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Corso')),
            ],
            options={
                'verbose_name': 'Approvazione',
                'verbose_name_plural': 'Approvazioni',
            },
        ),
    ]