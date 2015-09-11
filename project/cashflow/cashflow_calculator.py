import datetime
from trancheur.models import Contract, Trade, Bond
from .models import Cashflow
from libor.models import Libor
from trancheur.trancheur import Trancheur
from django.utils import timezone


class CashflowCreator():
	def __init__(self,bond):
		self.bond = bond

	def monthly_money_market_coupon_rate(self,date):
		libor = Libor()
		libor_rate = libor.get_latest_rate(date)
		total = libor_rate + Trancheur(self.bond).money_market_spread
		return total / 12

	def monthly_money_market_cashflow(self,date):
		money_market_face = Trancheur(self.bond).money_market_investment()
		return money_market_face * self.monthly_money_market_coupon_rate(date)

	def create_cashflows(self):
		date = self.bond.dated_date
		while date < timezone.now():
			n = 0
			accumulated_money_market_cashflows = 0
			while n < 6:
				coupon = round(self.monthly_money_market_cashflow(date),2)
				accumulated_money_market_cashflows += coupon
				money_market_cashflow = Cashflow(amount = coupon, date = date, type_of = "money_market", bond = self.bond)
				money_market_cashflow.save()
				date = date + timezone.timedelta(days = 30)	
				n += 1
			residual_interest = float(self.bond.face * self.bond.coupon/2) - accumulated_money_market_cashflows
			residual_cashflow = Cashflow(amount = residual_interest, date = date, type_of = "residual", bond = self.bond)
			residual_cashflow.save()	

	def residual_cashflows(self):
		cashflows = []
		num_residuals = self.bond.num_residuals()
		for cashflow in self.bond.cashflows.filter(type_of="residual"):
			cashflows.append({'amount':round(cashflow.amount / num_residuals,2) , 'date': cashflow.date})
		return cashflows
