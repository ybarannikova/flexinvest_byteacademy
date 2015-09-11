from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
	user = models.ForeignKey(User, related_name='transactions')
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	time = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length = 20)
	description = models.CharField(max_length = 100)

	def __str__(self):
		return self.category + " " + str(self.amount)