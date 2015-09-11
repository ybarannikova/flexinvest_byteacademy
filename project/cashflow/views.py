from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from cashflow.models import Cashflow
from trancheur.models import Bond, Contract, Trade, MoneyMarket, Residual
import datetime

# Create your views here.

class UserCashflows(View):

    def get(self, request):
        user = User.objects.get(id=request.session['user_id'])
        trades = Trade.objects.filter(buyer=user)
        for trade in trades:
            cashflows = Cashflow.objects.filter(contract = trade.contract)
            cashflows = [{'amount':cashflow.amount, 'date':cashflow.date, 'contract_id':cashflow.contract.id} for cashflow in cashflows]

        return JsonResponse({'cashflows':cashflows})
