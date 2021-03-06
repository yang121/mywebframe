# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 07:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='操作标题')),
                ('code', models.CharField(max_length=32, verbose_name='方法')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('img', models.ImageField(null=True, upload_to='', verbose_name='文章图片')),
                ('summary', models.CharField(max_length=255, verbose_name='文章简介')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article_type_id', models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'OpenStack'), (4, 'Golang')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='所属文章')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, unique=True, verbose_name='个人博客前缀')),
                ('theme', models.CharField(max_length=72, verbose_name='博客主题')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='评论文章')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='repository.Comment', verbose_name='回复评论')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='菜单标题')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p', to='repository.Menu', verbose_name='父菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, unique=True, verbose_name='权限标题')),
                ('url', models.CharField(max_length=128, verbose_name='URL正则')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='repository.Menu', verbose_name='所属菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Permission2Action2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='repository.Action', verbose_name='操作')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='repository.Permission', verbose_name='权限URL')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, unique=True, verbose_name='角色')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='UpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.BooleanField(verbose_name='是否赞')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('nickname', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='昵称')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='邮箱')),
                ('telephone', models.CharField(max_length=32, unique=True, verbose_name='手机号码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gender', models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], null=True, verbose_name='性别')),
                ('avatar', models.CharField(blank=True, max_length=128, null=True, verbose_name='头像路径')),
            ],
        ),
        migrations.CreateModel(
            name='User2Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.Role', verbose_name='角色')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='repository.User', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='repository.User', verbose_name='粉丝')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.User', verbose_name='博主')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, unique=True, verbose_name='组名')),
            ],
        ),
        migrations.AddField(
            model_name='user2group',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.UserGroup', verbose_name='组'),
        ),
        migrations.AddField(
            model_name='user2group',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='repository.User', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='user',
            name='fans',
            field=models.ManyToManyField(related_name='u2f', through='repository.UserFans', to='repository.User', verbose_name='粉丝们'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ManyToManyField(related_name='u2g', through='repository.User2Group', to='repository.UserGroup', verbose_name='用户组'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(related_name='u2r', through='repository.User2Role', to='repository.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.User', verbose_name='赞或踩用户'),
        ),
        migrations.AddField(
            model_name='permission2action2role',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p2as', to='repository.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.User', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.User'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Category', verbose_name='文章类型'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(through='repository.Article2Tag', to='repository.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('user', 'follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='user2role',
            unique_together=set([('user', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='user2group',
            unique_together=set([('user', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('article', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='permission2action2role',
            unique_together=set([('permission', 'action', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
