from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from trancheur.models import Contract, Bond

class Command(BaseCommand):
    groups = {
        'Investor': [
        {
            'codename': 'can_view_investment_details',
            'name': 'Can View Investment Details',
            'content_type': ContentType.objects.get_for_model(Contract),
        },
        {
            'codename': 'can_own_contracts',
            'name': 'Can Own Contracts',
            'content_type': ContentType.objects.get_for_model(Contract),
        },],
        'Analyst': [
        {
            'codename': 'can_tranche',
            'name': 'Can Tranche',
            'content_type': ContentType.objects.get_for_model(Bond),
        },],
    }
    help = 'Creates the user groups needed for authentication and templating'

    def handle(self, *args, **options):
        for groupname, permissions in self.groups.items():
            group = Group(name=groupname)
            group.save()
            for permission in permissions:
                permission = Permission.objects.create(**permission)
                group.permissions.add(permission)
            self.stdout.write('Successfully created group "%s"' % groupname)
