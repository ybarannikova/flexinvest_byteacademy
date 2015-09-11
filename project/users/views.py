from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from users.forms import UpdateForm

from django.contrib.auth.models import User, Group

from bank.models import Transaction

class Login(View):
    template = 'users/login.html'
    form = AuthenticationForm

    def get(self, request):
        return render(request, self.template, {'login_form':self.form()})

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/flex/')
            else:
                return render(request, self.template, {'login_error':"Account no longer active.", 'login_form':self.form()})
        else:
            return render(request, self.template, {'login_error':"Invalid login information.", 'login_form':self.form()})

class Register(View):
    template = 'users/register.html'
    form = UserCreationForm

    def get(self, request):
        return render(request, self.template, {'register_form':self.form})

    def post(self, request):
        form = self.form(request.POST)
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, self.template, {'registration_error': "Username already taken.", 'register_form': self.form()})
        except:
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Investor')
                user.groups.add(group)
                transaction = Transaction(user=user, amount=100000, category='DEPOSIT', description='Welcome gift from Flex.')
                transaction.save()
                return redirect('/login/')
            else:
                return render(request, self.template, {'registration_error':'Invalid input - Please populate all fields on the form.', 'register_form':self.form()})

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')
