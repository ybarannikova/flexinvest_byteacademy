from django.db import models

class Cashflow(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    type_of = models.CharField(max_length = 20)
    bond = models.ForeignKey('trancheur.Bond', related_name='cashflows')
