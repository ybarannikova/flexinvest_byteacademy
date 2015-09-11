from trancheur.trancheur import Trancheur
from trancheur.models import Bond

class QueryTranches:
    def __init__(self):
        self.query_dict = {
            "11_15": dict(minimum=.11, maximum=.15),
            "15_19": dict(minimum=.15, maximum=.19),
            "19_23": dict(minimum=.19, maximum=.23),
            "23_27": dict(minimum=.23, maximum=.27),
            }

    def get_all_unauctioned_bonds_by_query(self, query_list):
        filtered_bonds = []
        for bond in Bond.get_all_unauctioned_bonds():
            for query in query_list:
                if self.query_dict[query]["minimum"] < Trancheur(bond).est_yield() < self.query_dict[query]["maximum"]:
                    filtered_bonds.append(bond)
                    break
        return filtered_bonds