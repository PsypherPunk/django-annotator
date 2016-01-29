# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0004_auto_20160129_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='uri',
            field=models.CharField(null=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='user',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
