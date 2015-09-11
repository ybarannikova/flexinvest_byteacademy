from django.core.management.base import BaseCommand, CommandError
from trancheur.seed import Seed

class Command(BaseCommand):
    help = "seeds the database with bonds, contracts and users"

    def handle(self, *args, **kwargs):
        seeds = {
            'flex_investor_user': Seed.flex_investor_user,
            'flex_analyst_user': Seed.flex_analyst_user,
            'scenario1': Seed.scenario1,
            'scenario2': Seed.scenario2,
            'update_cache': Seed.update_cache,
        }
        if args:
            for arg in args:
                self.stdout.write('starting {}'.format(seeds[arg]))
                seeds[arg]()
                self.stdout.write('{} complete'.format(seeds[arg]))
        else:
            self.stdout.write('starting full seed')
            Seed.flex_investor_user()
            Seed.flex_analyst_user()
            Seed.scenario1()
            Seed.scenario2()
            Seed.update_cache()
            self.stdout.write('full seed complete')

