import factory

class BondFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.Bond'

class ContractFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.Contract'

class TradeFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.Trade'

class MoneyMarketFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.MoneyMarket'

class ResidualFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.Residual'

class BondPriceFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'trancheur.BondPrice'
