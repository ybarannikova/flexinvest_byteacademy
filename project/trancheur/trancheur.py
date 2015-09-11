from trancheur.models import Bond, Contract, Residual, MoneyMarket
from libor.models import Libor
import datetime

class Trancheur:
    def __init__(self, bond, residual_to_floater_gearing=4, residual_face=10000, money_market_spread=.0005):
        self.bond = bond
        self.floater_allocation = residual_to_floater_gearing / (residual_to_floater_gearing + 1)
        self.residual_allocation = 1 / (residual_to_floater_gearing + 1)
        self.residual_face = residual_face
        self.money_market_spread = money_market_spread

    def total_cost(self):
        return float(self.bond.face * self.bond.initial_price)

    def number_of_residual_contracts(self):
        return int(self.total_cost() * self.residual_allocation // self.residual_face)

    def residual_investment(self):
        return self.residual_face * self.number_of_residual_contracts()

    def money_market_investment(self):
        return self.total_cost() - self.number_of_residual_contracts() * self.residual_face

    def money_market_coupon(self):
        return round(Libor().most_recent_libor_rate() + self.money_market_spread, 4)

    def est_yield(self):
        money_market_annual_revenue = float(self.money_market_coupon()) * float(self.money_market_investment())
        bond_annual_revenue = float(self.bond.coupon) * float(self.bond.face)
        residual_annual_revenue = bond_annual_revenue - money_market_annual_revenue
        est_yield = float(residual_annual_revenue / self.residual_investment())
        return round(est_yield, 3)


    def originate_contracts(self):
        for i in range(self.number_of_residual_contracts()):
            residual_contract = Residual(
                    face = self.residual_face,
                    bond = self.bond,
                    payments_per_year = 2)
            residual_contract.save()

        money_market_contract = MoneyMarket(
            face = self.money_market_investment(),
            issuance_date = self.bond.dated_date,
            maturity = self.bond.dated_date + datetime.timedelta(days = 30),
            bond = self.bond,
            coupon = self.money_market_coupon())
        money_market_contract.save()
