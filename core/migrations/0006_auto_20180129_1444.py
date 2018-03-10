# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180107_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='author',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='director',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='retrieval_date',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_tag',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='url',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='year',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sourceexcerpt',
            name='begin_time',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sourceexcerpt',
            name='end_time',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sourceexcerpt',
            name='pages',
            field=models.TextField(blank=True),
        ),
    ]