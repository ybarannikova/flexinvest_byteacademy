from trancheur.models import Trade, Contract, Residual
from users.models import User
from django.utils import timezone
from bank.models import Transaction

class Trader:

    @staticmethod
    def has_valid_num_available_contracts(bond, num_contracts_requested):
        num_contracts = Residual.objects.filter(bond=bond, is_sold=False).count()
        if num_contracts_requested <= num_contracts:
            return True
        else:
            return False

    @staticmethod
    def total_trade_amount(bond, num_contracts):
        return float(bond.residual_face() * num_contracts)

    @staticmethod
    def make_first_trades(buyer, bond, num_contracts, price=1):
        seller = User.objects.get(username="flex")
        trade_ids = []
        for count in range(num_contracts):
            contract = Residual.objects.filter(bond=bond, is_sold=False)[0]
            trade = Trade(
                buyer=buyer,
                seller=User.objects.get(username="flex"),
                contract=contract, 
                price=price, 
                time=timezone.now()
            )
            trade.save()
            print("1 of 4 - Trade Saved.")
            transaction = Transaction(
                user=buyer,
                amount= -(contract.face * trade.price),
                category= "PURCHASE",
                description= "Primary purchase of {} contract".format(bond.__str__()),
            )
            transaction.save()
            print("2 of 4 - Transaction Saved.")
            contract.save()
            print("3 of 4 - Contract Saved.")
            bond.bondcache.save()
            print("4 of 4 - Bondcache Saved.")
            trade_ids.append(trade.id)
        return trade_ids


