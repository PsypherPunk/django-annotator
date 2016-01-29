# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_auto_20160129_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='range',
            name='annotation',
            field=models.ForeignKey(to='annotation.Annotation', related_name='ranges'),
        ),
    ]
