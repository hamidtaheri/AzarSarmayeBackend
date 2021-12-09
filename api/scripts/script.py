# import api

from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now

from api.models import *

# 1400/01/01        2021-03-21
# 1400/01/31        2021-04-20

# 1400/02/01        2021-04-21
# 1400/02/31        2021-05-21

# 1400/03/01        2021-05-22
# 1400/03/31        2021-06-21

# 1400/04/01        2021-06-22
# 1400/04/31        2021-07-22

# 1400/05/01        2021-07-23
# 1400/05/31        2021-08-22

# 1400/06/01        2021-08-23
# 1400/06/31        2021-09-22
az_date = sh2m('1400/07/01')
ta_date = sh2m('1400/07/30')


# print(now().strftime('%y-%m-%d_%H-%M-%S'))
# print(datetime.date.today())
# print(datetime.date.today() + datetime.timedelta(53))
# list_sod, sum_sod = mohasebe_sod_1_nafar(325, az_date, ta_date)
# print(sum_sod)

# mohasebe_sod_all(az_date, ta_date)

# mohasebe_sod_moarefi_all(az_date, ta_date)

def show_group_permissions(group: Group):
    permissions = group.permissions.all()
    for p in permissions:
        print(p.name)


def show_group_users(group: Group):
    users = group.user_set.all()
    for u in users:
        print(u.username)


def show_all_groups():
    groups = Group.objects.all()
    for g in groups:
        print(g.name)
        show_group_permissions(g)
        show_group_users(g)


def show_all_permissions():
    permission = Permission.objects.all()
    for p in permission:
        print(p.name)


# show_all_groups()

# show_all_permissions()


def days_after_transaction_start():
    for tr in Transaction.objects.filter(kind_id=1):
        tr: Transaction = tr
        tr_date = tr.effective_date
        now_date = now().date()
        diff = (now_date - tr_date).days
        print(f'{tr.Tarikh_Moaser} {tr.effective_date} {diff}')


from django.contrib.auth import get_user_model


def reset_password(u, password):
    try:
        user = get_user_model().objects.get(username=u)
    except:
        return "User could not be found"
    user.set_password(password)
    user.save()
    print("Password has been changed successfully")
    return "Password has been changed successfully"


# reset_password("superadmin", "abc*123")

# StateLog.objects.all()
user1: User = User.objects.get(id=1)
tr: Transaction = Transaction.objects.get(id=11466)
print(tr)
tr.state = 'START'
tr.created_by = user1
tr.save()
