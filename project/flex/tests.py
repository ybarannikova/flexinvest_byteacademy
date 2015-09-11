from django.test import TestCase, Client
from django.contrib.auth.models import User
from trancheur.models import Bond, Contract, Trade, MoneyMarket, Residual
from trancheur.trancheur import Trancheur
from django.utils import timezone
from trancheur.fixtures import BondFactory, ContractFactory, TradeFactory, MoneyMarketFactory, ResidualFactory, BondPriceFactory
import json
import pprint

# Create your tests here.

pp = pprint.PrettyPrinter(indent=4)
kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}

class FlexTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User()
        self.username = 'adickens'
        self.password = 'password'

        print ("=====SETTING UP=====")

    def test_investing_view(self):
        response = self.client.get('/flex/investing/')
        self.assertEqual(response.request['REQUEST_METHOD'],'GET')
        self.assertEqual(response.status_code, 200)

    def test_portfolio_view(self):
        response = self.client.get('/flex/portfolio/')
        self.assertEqual(response.request['REQUEST_METHOD'],'GET')
        self.assertEqual(response.status_code, 200)

    def test_account_view(self):
        response = self.client.get('/flex/account/')
        self.assertEqual(response.request['REQUEST_METHOD'],'GET')
        self.assertEqual(response.status_code, 200)

    def test_client_registration(self):
        response = self.client.post('/register/', {'username':self.username, 'password':self.password}, **kwargs)
        self.assertEqual(response.request['REQUEST_METHOD'],'POST')
        self.assertEqual(response.request['PATH_INFO'], '/register/')
        self.assertEqual(response.status_code, 200)

    def test_client_login(self):
        response = self.client.post('/login/', {'username':self.username, 'password':self.password}, **kwargs)
        self.assertEqual(response.request['REQUEST_METHOD'],'POST')
        self.assertEqual(response.request['PATH_INFO'], '/login/')
        self.assertEqual(response.status_code, 200)

    # def test_contract_details(self):
    #     response = self.client.get('/flex/portfolio/contract', {'contract
    #     ':67}, **kwargs)
    #     pp.pprint(response.request)
    #     self.assertEqual(response.request['REQUEST_METHOD'],'GET')
    #     self.assertEqual(response.status_code, 200)

    # def test_get_activity(self):
    #     data = {'amount':50000.00, 'date':timezone.now, 'description':'Deposit to account', 'category':'DEPOSIT'}
    #     response = self.client.get('/flex/portfolio/activity', data=data, **kwargs)
    #     # pp.pprint(response.request)
    #     self.assertEqual(response.status_code, 200)
