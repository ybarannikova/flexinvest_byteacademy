from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from trancheur.models import Bond, Contract, Trade, Residual, BondPrice
from users.forms import UpdateForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, PasswordResetForm
from users.models import User
from cashflow.cashflow_calculator import CashflowCreator
from .helper import QueryTranches
from .models import BondCache
import datetime
from trancheur.forms import BondForm
from .services.trader import Trader
from .services.quantifier import Quantifier

class InvestingApi(View):

    def get(self, request):
        queries = request.META['QUERY_STRING'].split("+")
        if queries[0]:
            data = BondCache.get_all_unauctioned_bonds_by_query_as_json(queries)
        else:
            data = BondCache.get_all_unauctioned_bonds_as_json()
        return JsonResponse(data)

class Index(View):

    def get(self, request):
        return redirect("/flex/investing/")

class Investing(View):

    def get(self, request):
        return render(request, "flex/investing.html")

class Portfolio(View):

    def get(self, request):
        return render(request, "flex/portfolio.html")

class Investments(View):

    def get(self, request):
        user = self.request.user
        last_purchases = [purchase for purchase in user.purchases.all() if purchase.contract.trades.latest().buyer == user]
        context_dict = [{'contract':purchase.contract.id, 'price':round(purchase.price * purchase.contract.face, 2), 'current_value': Quantifier().contract_current_value(purchase.contract), 'maturity': purchase.contract.bond.maturity, 'purchase_date': purchase.time.strftime("%Y-%m-%d %H:%M:%S"), 'change_in_value': Quantifier().contract_value_change(purchase)} if purchase.contract.bond.dated_date < datetime.date.today() else {'contract':purchase.contract.id, 'price':round(purchase.price * purchase.contract.face, 2), 'current_value': round(purchase.price * purchase.contract.face, 2), 'maturity': purchase.contract.bond.maturity, 'purchase_date': purchase.time.strftime("%Y-%m-%d %H:%M:%S"), 'change_in_value': 0} for purchase in last_purchases]
        return JsonResponse({'investments':context_dict})    

class Contract(View):

    def get(self, request):
        contract = Residual.objects.get(id = request.GET['contract'])
        cashflows = CashflowCreator(contract.bond).residual_cashflows()
        cashflows_since_purchase = [cashflow for cashflow in cashflows if cashflow['date'] > contract.trades.latest().time.date()]
        total = (sum(item['amount'] for item in cashflows_since_purchase))
        if len(cashflows_since_purchase) > 0:
            return JsonResponse({'data':{'cashflows':cashflows_since_purchase,'total':total, 'average_return': Quantifier().average_annualized_cashflow_yield(cashflows_since_purchase,contract), 'current_value':Quantifier().contract_current_value(contract)}})   
        else:
            return JsonResponse({'data': {'message': 'no cashflows'}})

class Activity(View):

    def get(self, request):
        transactions = request.user.transactions.all()
        context_dict = [{'date':transaction.time.strftime("%Y-%m-%d %H:%M:%S"), 'category': transaction.category, 'description':transaction.description, 'amount': transaction.amount} for transaction in transactions]    
        balance = User.objects.get(username = request.user.username).get_balance()
        return JsonResponse({'transactions':context_dict, 'balance': balance})

class Account(View):
    form = PasswordChangeForm

    def get(self, request):
        return render(request, "flex/account.html", {'form':self.form(user=request.user)})

    def post(self, request):
        form = self.form(user=request.user, data=request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return render(request, 'flex/account.html', {'updated': 'Account updated.', 'form':self.form(user=request.user)})
        else:
            return render(request, 'flex/account.html', {'error': 'Invalid password combination.', 'form':self.form(user=request.user)})

class Purchase(View):

    def post(self, request):
        bond = Bond.objects.get(id=request.POST['tranche_id'])
        num_contracts = int(request.POST['num_contracts'])
        user = User.objects.get(id=request.user.id)
        total_trade_amount = Trader.total_trade_amount(bond, num_contracts)
        if user.has_sufficient_funds(total_trade_amount):
            if Trader.has_valid_num_available_contracts(bond, num_contracts):
                trade_ids = Trader.make_first_trades(request.user, bond, num_contracts)
                request.session['trade_ids'] = trade_ids
                return redirect("/flex/purchase/")
            else:
                return render(request, "flex/investingconfirmation.html", {'error':'Trade error.'})
        else:
            return render(request, "flex/investingconfirmation.html", {'error':'Insufficient funds.'})

    def get(self, request):
        context_dict = dict(trades=[])
        for trade_id in request.session['trade_ids']:
            context_dict['trades'].append(Trade.objects.get(id=trade_id))
        del request.session['trade_ids']
        return render(request, "flex/investingconfirmation.html", context_dict)

class TrancheurView(View):
    form = BondForm

    def get(self, request):
        return render(request, "flex/trancheur.html", {'form': self.form()})
