# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 05:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LinuxChallenge', '0004_auto_20160329_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ['published_time']},
        ),
    ]
