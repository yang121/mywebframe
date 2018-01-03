# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_auto_20180103_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='img',
            field=models.FileField(upload_to='static/imgs/ad/', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='column',
            name='img',
            field=models.FileField(upload_to='static/imgs/cols/', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='img',
            field=models.FileField(upload_to='static/imgs/goods/', verbose_name='图片'),
        ),
    ]
