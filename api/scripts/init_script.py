from django.contrib import auth
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now

from api.models import *


# superuser: User = User(username='superadmin', is_superuser=True, is_staff=True)
# superuser.set_password('Admin123')
# superuser.save()
def set_wf_state_to_converted():
    print(f'start:{now()}')
    for p in Profile.objects.all():
        p.state = 'start'
        p.to_convert()
        p.save()
    print(f'profile end:{now()}')

    user1: User = User.objects.get(username='superadmin')
    for t in Transaction.objects.all():
        # تبدیل تاریخ های تراکنش از شمسی به میلادی
        t.date = sh2m(t.tarikh)
        t.effective_date = sh2m(t.Tarikh_Moaser)
        t.presenter_effective_date = sh2m(t.Tarikh_Moaser_Moaref)
        t.state = 'start'
        t.to_convert()
        t.created_by = user1
        t.created = now()
        t.save()

    print(f'transaction end:{now()}')


def set_costumer_group_permisions(name: str):
    customer_group: Group = Group.objects.get(name=name)
    customer_perms: list[Permission] = []
    customer_perms.append(Permission.objects.get(codename='STUFF_ADDED_WF_STATE'))
    customer_perms.append(Permission.objects.get(codename='CUSTOMER_ADDED_WF_STATE'))
    customer_perms.append(Permission.objects.get(codename='STUFF_CHECKED_WF_STATE'))
    customer_perms.append(Permission.objects.get(codename='STUFF_CONFIRMED_WF_STATE'))
    customer_perms.append(Permission.objects.get(codename='CUSTOMER_CONFIRMED_WF_STATE'))
    customer_perms.append(Permission.objects.get(codename='WF_TRANSITION_PROFILE_START_TO_CUSTOMER_ADDED'))
    customer_perms.append(Permission.objects.get(codename='WF_TRANSITION_PROFILE_STUFF_ADDED_TO_COSTUMER_CONFIRMED'))
    customer_perms.append(Permission.objects.get(codename='WF_TRANSITION_PROFILE_STUFF_ADDED_TO_STUFF_ADDED'))
    # customer_perms.append(Permission.objects.get(codename=''))

    customer_group.permissions.set(customer_perms)


# set_costumer_group_permisions('customer_group')
