from trancheur.models import Contract, Trade
from cashflow.models import Cashflow
import datetime

cashflow1 = Cashflow(
    amount = 140000.00,
    date = datetime.date(2016, 1, 15),
    contract = Trade.objects.last().contract
)

cashflow2 = Cashflow(
    amount = 140000.00,
    date = datetime.date(2016, 7, 15),
    contract = Trade.objects.last().contract
)

def seed():
    cashflow1.save()
    cashflow2.save()

# seed()
