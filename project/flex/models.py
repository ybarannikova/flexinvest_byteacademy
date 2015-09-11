from django.db import models
from trancheur.models import Bond
from trancheur.trancheur import Trancheur
import json

class BondCache(models.Model): 
    bond = models.OneToOneField(Bond)
    is_available = models.BooleanField(default=True)
    data = models.TextField()

    def save(self, *args, **kwargs):
        if self.bond.num_available_residuals() > 0:
            data = dict(
                funded =  float(self.bond.percent_residuals_funded()),
                est_yield = float(Trancheur(self.bond).est_yield()),
                term = int(self.bond.term()),
                tranche = float(Trancheur(self.bond).residual_investment()),
                amount_left = int(self.bond.amount_left_of_residuals()),
                time_left = int(self.bond.days_to_auction()),
                tranche_id = self.id,
                maturity_day = str(self.bond.maturity.day).zfill(2),
                maturity_month = str(self.bond.maturity.month).zfill(2),
                maturity_year = str(self.bond.maturity.year), 
                payments_per_year = self.bond.payments_per_year,
                face = self.bond.residual_face(),
                dated_date_day = str(self.bond.dated_date.day).zfill(2),
                dated_date_month = str(self.bond.dated_date.month).zfill(2),
                dated_date_year = str(self.bond.dated_date.year),
                num_available = self.bond.num_available_residuals(),
            )
            self.data = json.dumps(data)
        else:
            self.is_available = False
        super(BondCache, self).save(*args, **kwargs)

    @classmethod
    def get_all_unauctioned_bonds_as_json(cls):
        data = []
        for bond_cache in cls.objects.filter(is_available=True):
            data.append(json.loads(bond_cache.data))
        return dict(data=data)

    @classmethod
    def get_all_unauctioned_bonds_by_query_as_json(cls, queries):

        query_reference = dict()
        for query in queries:
            parsed_query = query.split("_")
            query_type = "_".join(parsed_query[0:-2])
            if not query_reference.get(query_type):
                query_reference[query_type] = list()
            min_max_tuple = (float(parsed_query[-2]), float(parsed_query[-1]))
            query_reference[query_type].append(min_max_tuple)

        filtered_data = [[],]
        for count, query_type in enumerate(query_reference):
            if count == 0:
                for bond_cache in cls.objects.filter(is_available=True):
                    data = json.loads(bond_cache.data)
                    for query_range in query_reference[query_type]:
                        if query_range[0] <= data[query_type] <= query_range[1]:
                            filtered_data[0].append(data)
            else:
                filtered_data_per_query = list()
                for data in filtered_data[-1]:
                    for query_range in query_reference[query_type]:
                        if query_range[0] <= data[query_type] <= query_range[1]:
                            filtered_data_per_query.append(data)
                filtered_data.append(filtered_data_per_query)
        return dict(data=filtered_data[-1])
            

