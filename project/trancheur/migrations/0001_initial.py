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
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('cusip', models.CharField(max_length=9, unique=True)),
                ('face', models.DecimalField(max_digits=15, decimal_places=2)),
                ('coupon', models.DecimalField(max_digits=15, decimal_places=5)),
                ('initial_price', models.DecimalField(max_digits=6, decimal_places=5)),
                ('dated_date', models.DateField()),
                ('auction_date', models.DateTimeField()),
                ('maturity', models.DateField()),
                ('payments_per_year', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BondPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('price', models.DecimalField(max_digits=6, decimal_places=5)),
                ('date', models.DateField()),
                ('bond', models.ForeignKey(related_name='prices', to='trancheur.Bond')),
            ],
            options={
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('face', models.DecimalField(max_digits=15, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type_of', models.CharField(max_length=20)),
                ('is_sold', models.BooleanField(default=False)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoneyMarket',
            fields=[
                ('contract_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, to='trancheur.Contract', serialize=False)),
                ('coupon', models.DecimalField(max_digits=15, decimal_places=5)),
                ('issuance_date', models.DateField()),
                ('maturity', models.DateField()),
            ],
            options={
            },
            bases=('trancheur.contract',),
        ),
        migrations.CreateModel(
            name='Residual',
            fields=[
                ('contract_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, to='trancheur.Contract', serialize=False)),
                ('payments_per_year', models.IntegerField()),
            ],
            options={
            },
            bases=('trancheur.contract',),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('price', models.DecimalField(max_digits=6, decimal_places=5)),
                ('time', models.DateTimeField()),
                ('buyer', models.ForeignKey(related_name='purchases', to=settings.AUTH_USER_MODEL)),
                ('contract', models.ForeignKey(related_name='trades', to='trancheur.Contract')),
                ('seller', models.ForeignKey(related_name='sales', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'time',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contract',
            name='bond',
            field=models.ForeignKey(related_name='contracts', to='trancheur.Bond'),
            preserve_default=True,
        ),
    ]
