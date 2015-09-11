from trancheur.trancheur import Trancheur


class Quantifier:

	@staticmethod
	def contract_current_value(contract):
		muni_value = float(contract.bond.prices.latest().price * contract.bond.face)
		residual_value = muni_value - Trancheur(contract.bond).money_market_investment()
		return round(residual_value / Trancheur(contract.bond).number_of_residual_contracts(),2)

	@staticmethod
	def contract_value_change(purchase):
		p1 = float(purchase.price * purchase.contract.face)
		p2 = Quantifier.contract_current_value(purchase.contract)
		return ((p2-p1)/p1 * 100)

	@staticmethod
	def average_annualized_cashflow_yield(list_of_cashflows,contract):
		annualized_returns = [(1 + i['amount'] / contract.face) ** 2 - 1  for i in list_of_cashflows]
		if len(annualized_returns) == 0:
		    return 0
		else:    
		    average_return = sum(annualized_returns)/len(annualized_returns)
		    return round(average_return*100,3)  
