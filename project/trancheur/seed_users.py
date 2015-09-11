from .models import Bond, Contract, Residual, MoneyMarket, Trade 
from django.contrib.auth.models import User, Group
from bank.models import Transaction
from faker import Faker
import datetime
from django.utils import timezone
from cashflow.models import Cashflow
from cashflow.cashflow_calculator import CashflowCreator

fake = Faker()

class Seed_users:
	def __init__(self,bond):
		self.bond = bond
		self.contracts = Residual.objects.filter(bond = self.bond)
		self.owner = User.objects.get(username = 'flex')
		self.cashflows = CashflowCreator(self.bond).residual_cashflows()
	#the number of users is equal to a number of residual contracts in a bond
	def create_users_and_sell_contracts(self):
		print("Creating users, giving them a deposit of $50,000 and selling each one contract...")
		for contract in self.contracts:
			username = fake.user_name()
			user = User(username=username)
			user.set_password("password")
			try:
				user.save()
				group = Group.objects.get(name='Investor')
				user.groups.add(group)
			except:
				user = User.objects.get(username=username)
			group = Group.objects.get(name='Investor')
			user.groups.add(group)
			deposit = Transaction(user = user, amount = 50000, category = 'DEPOSIT', description = "Deposit to account")
			deposit.save()
			time = timezone.now().replace(year = contract.bond.dated_date.year, month = contract.bond.dated_date.month, day = contract.bond.dated_date.day)
			contract_sale = Trade(buyer = user, seller = self.owner, contract = contract, price = 1, time = time)
			contract_sale.save()
			sale = Transaction(user = user, amount = -(contract_sale.price * contract_sale.contract.face), time = contract_sale.time, category = 'PURCHASE', description = "Initial purchase of one contract")
			sale.save()
			for cashflow in self.cashflows:
				interest_revenue = Transaction(user = user, amount = cashflow['amount'], time = cashflow['date'], category = "INTEREST", description = "Interest revenue on FLEX contract " + str(contract.id))
				interest_revenue.save()
