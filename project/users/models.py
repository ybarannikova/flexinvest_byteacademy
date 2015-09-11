from django.db import models
from django.contrib.auth.models import User

class User(User):
    class Meta:
        proxy = True

    def get_all_money_spent(self):
        amount_spent = sum([float(trade.price) * float(trade.contract.face) for trade in self.purchases.all()])    
        return round(amount_spent, 2)

    def get_balance(self):
        balance = sum([float(transaction.amount) for transaction in self.transactions.all()])
        return round(balance, 2)

    def has_sufficient_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        else:
            return False