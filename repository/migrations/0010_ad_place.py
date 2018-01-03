# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20180103_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='place',
            field=models.IntegerField(blank=True, choices=[(1, '第一位'), (2, '第二位'), (3, '第三位'), (4, '第四位'), (5, '第五位'), (6, '第六位')], null=True, unique=True, verbose_name='位置'),
        ),
    ]