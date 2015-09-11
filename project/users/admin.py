from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission

from trancheur.models import Bond, MoneyMarket, Residual, Trade
from cashflow.models import Cashflow

class AdminSite(AdminSite):
    site_title = 'FlexInvest Admin'
    index_title = 'Home'
    branding = "admin/logo.png"

admin_site = AdminSite()

def deactivate_account(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_account.short_description = "Deactivate selected users"

def activate_account(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_account.short_description = "Activate selected users"

class UserAdmin(UserAdmin):
    list_display = ('username', 'is_active', 'last_login', 'date_joined',)
    list_filter = ('groups', 'is_active',)
    date_hierarchy = 'date_joined'
    actions = [deactivate_account, activate_account]

admin_site.register(User, UserAdmin)
admin_site.register(Permission)
admin_site.register(Group)
admin_site.register(Bond)
admin_site.register(MoneyMarket)
admin_site.register(Residual)
admin_site.register(Trade)
admin_site.register(Cashflow)
