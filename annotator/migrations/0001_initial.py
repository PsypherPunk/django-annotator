# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('annotator_schema_version', models.CharField(default='v1.0', max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('quote', models.TextField()),
                ('uri', models.CharField(max_length=4096, blank=True)),
                ('user', models.CharField(max_length=128, blank=True)),
                ('consumer', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.CharField(max_length=128)),
                ('end', models.CharField(max_length=128)),
                ('startOffset', models.IntegerField()),
                ('endOffset', models.IntegerField()),
                ('annotation', models.ForeignKey(to='annotator.Annotation', related_name='ranges')),
            ],
        ),
    ]
