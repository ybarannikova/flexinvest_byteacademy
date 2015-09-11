from .models import Bond, BondPrice
from trancheur.trancheur import Trancheur
from trancheur.seed_users import Seed_users
import csv
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group
from trancheur.trancheur import Trancheur
from cashflow.cashflow_calculator import CashflowCreator
import random
from flex.models import BondCache


class Seed:

    @classmethod
    def raw_date_to_date_object(cls, string):
        parsed_date = string.split('/')
        month = int(parsed_date[0].zfill(2))
        day = int(parsed_date[1].zfill(2))
        year = int('20' + parsed_date[2])
        return timezone.now().replace(year=year, month=month, day=day)

    @classmethod
    def seed_bond_prices_from_csv(cls, bond, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                date = cls.raw_date_to_date_object(row[0])
                price = float(row[1])
                bond_price = BondPrice(
                    date=date,
                    price=price,
                    bond=bond,
                )
                bond_price.save()

    @classmethod
    def flex_investor_user(cls):
        user = User(username="flex")
        user.set_password("password")
        user.save()
        group = Group.objects.get(name='Investor')
        user.groups.add(group)

    @classmethod
    def flex_analyst_user(cls):
        user = User(username="flex.analyst")
        user.set_password("password")
        user.save()
        group = Group.objects.get(name='Analyst')
        user.groups.add(group)

    @classmethod
    def scenario1(cls):
        bonds = [
            {'filename':'trancheur/seeds/64966JNF9.csv',
             'instance': Bond(
                    cusip='64966JNF9',
                    face=5000000,
                    coupon=.05,
                    dated_date=timezone.now().replace(year=2011, month=8, day=9),
                    auction_date = timezone.now().replace(year=2011, month=8, day=9) - timezone.timedelta(days=7),
                    maturity=timezone.now().replace(year=2032, month=8, day=1),
                    payments_per_year=2,
                    initial_price = 1.04884,
                    )
            },
            {'filename':'trancheur/seeds/650035VB1.csv',
             'instance': Bond(
                    cusip='650035VB1',
                    face=10000000,
                    coupon=.05838,
                    dated_date=timezone.now().replace(year=2010, month=12, day=8),
                    auction_date = timezone.now().replace(year=2010, month=12, day=8) - timezone.timedelta(days=7),
                    maturity=timezone.now().replace(year=2040, month=3, day=15),
                    payments_per_year=2,
                    initial_price = 1,
                    )
            },
        ]
        "This creates bonds issued in the past. Seeds users, one for each contract created."
        for bond in bonds:
            bond['instance'].save()
            cls.seed_bond_prices_from_csv(bond['instance'], bond['filename'])
            Trancheur(bond['instance']).originate_contracts()
            CashflowCreator(bond['instance']).create_cashflows()
            Seed_users(bond['instance']).create_users_and_sell_contracts()
            bond['instance'].bondcache = BondCache(is_available=False)
            bond['instance'].bondcache.save()



    @classmethod
    def scenario2(cls):
        num_bonds = 20
        for count in range(num_bonds):
            cusip = "FLXBOND" + str(count).zfill(2)
            face = random.randrange(50000,2000000,10000)
            coupon = 3.75 + (random.randint(0, 6) * .25)
            initial_price = random.randint(98, 119) / 100
            auction_date = timezone.now() + timezone.timedelta(days=random.randint(1,14))
            dated_date = auction_date + timezone.timedelta(days=10)
            maturity = dated_date + timezone.timedelta(days=random.randint(20,30)*365)
            payments_per_year = 2

            bond = Bond(
                cusip = cusip,
                face = face,
                coupon = coupon,
                initial_price = initial_price,
                auction_date = auction_date,
                dated_date = dated_date,
                maturity = maturity,
                payments_per_year = payments_per_year,
            )
            bond.save()
            Trancheur(bond).originate_contracts()
            bond.bondcache = BondCache()
            bond.save()
            bond.bondcache.save()

    @classmethod
    def update_cache(cls):
        for bond_cache in BondCache.objects.all():
            bond_cache.save()
        












