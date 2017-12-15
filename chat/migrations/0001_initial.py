# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chat_author')),
                ('companion', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chat_companion')),
                ('user_last_change', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='chat_user_last_change')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=250)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(to='chat.Chat')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('author', 'companion')]),
        ),
    ]
