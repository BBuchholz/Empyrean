# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180423_2108'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sourceexcerpttagging',
            unique_together=set([('excerpt', 'tag')]),
        ),
    ]
