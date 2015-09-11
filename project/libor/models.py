from django.db import models
import datetime
from .quandl import Quandl
from django.core.exceptions import ObjectDoesNotExist

class Libor(models.Model):
    date = models.DateField(unique=True)
    rate = models.DecimalField(max_digits=8, decimal_places=5)

    def seed_libor_database(self):
        print("Seeding libor database.")
        libor_list = Quandl().get_all_libor_rates_and_dates()
        for libor_dict in libor_list:
            try:
                Libor.objects.get(date=libor_dict['date'])
            except:
                libor = Libor(
                    date=libor_dict['date'],
                    rate=libor_dict['rate']
                )
                libor.save()
        print("")

    def get_most_recent_libor_object(self):
        day = 0
        while day < 30:
            date = datetime.date.today() - datetime.timedelta(day)
            try:
                return Libor.objects.get(date=date)
            except:
                day += 1
        self.seed_libor_database()

        return Libor.objects.latest('date')

    def most_recent_libor_rate(self):
        libor = self.get_most_recent_libor_object()
        return float(libor.rate)

    def most_recent_libor_date(self):
        libor = self.get_most_recent_libor_object()
        return libor.date

    def most_recent_libor_as_dict(self):
        libor = self.get_most_recent_libor_object()
        return {'date':libor.date, 'rate':float(libor.rate)}

    def get_rate_by_date(self, date_object):
        """
        Takes a datetime.date object,
        returns the corresponding libor rate as a float.
        If does not exist, returns None.
        """
        try:
            libor = Libor.objects.get(date=date_object)
            return float(libor.rate)
        except:
            try:
                self.seed_libor_database()
                libor = Libor.objects.get(date=date_object)
                return float(libor.rate)
            except:
                return None

    def get_latest_rate(self, date_object): 
        while True:
            try:
                libor = Libor.objects.get(date=date_object)
                return float(libor.rate)
            except ObjectDoesNotExist:
                date_object = date_object - datetime.timedelta(days = 1)
                continue
            break




