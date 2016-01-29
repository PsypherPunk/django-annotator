# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('annotator_schema_version', models.CharField(default='v1.0', max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('quote', models.TextField()),
                ('uri', models.CharField(max_length=4096)),
                ('user', models.CharField(max_length=128)),
                ('consumer', models.CharField(default='thedatashed', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start', models.CharField(max_length=128)),
                ('end', models.CharField(max_length=128)),
                ('startOffset', models.IntegerField()),
                ('endOffset', models.IntegerField()),
                ('annotation', models.ForeignKey(to='annotation.Annotation')),
            ],
        ),
    ]
