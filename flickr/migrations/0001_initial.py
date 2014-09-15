# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=100)),
                ('secret', models.CharField(max_length=100)),
                ('created', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('fetched', models.DateTimeField(null=True)),
                ('updated', models.DateTimeField()),
                ('username', models.CharField(max_length=100)),
                ('nsid', models.CharField(unique=True, max_length=20)),
                ('fullname', models.CharField(max_length=100)),
                ('feed_secret', models.CharField(unique=True, max_length=13)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=100)),
                ('secret', models.CharField(max_length=100)),
                ('created', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
