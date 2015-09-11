# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Libor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(unique=True)),
                ('rate', models.DecimalField(decimal_places=5, max_digits=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
