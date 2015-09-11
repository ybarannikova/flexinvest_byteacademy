# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trancheur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BondCache',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_available', models.BooleanField(default=True)),
                ('data', models.TextField()),
                ('bond', models.OneToOneField(to='trancheur.Bond')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
