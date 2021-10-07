# import api
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

# 1400/04601        2021-08-23
# 1400/06/31        2021-09-22
az_date = sh2m('1400/07/01')
ta_date = sh2m('1400/07/30')


def mohasebe_sod_all():
    for p in Profile.objects.all():
        mohasebe_sod_1_nafar(p.id)


def mohasebe_sod_1_nafar(a: int):
    m = Profile.objects.get(id=a)
    print(m)
    mo, so = m.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
    print(f'for {m.id} : {so}')


# print(datetime.date.today())
# print(datetime.date.today() + datetime.timedelta(53))

m = Profile.objects.get(id=2)
print(m)

transactions: QuerySet[Transaction] = Transaction.objects.filter(profile__presenter=m)
seporde = transactions.filter(kind=1).aggregate(seporde=Sum('amount'))['seporde']
marjo = transactions.filter(kind=2).aggregate(marjo=Sum('amount'))['marjo'] or 0
variz_sod = transactions.filter(kind=3).aggregate(variz_sod=Sum('amount'))['variz_sod']
bardasht_sod = transactions.filter(kind=4).aggregate(bardasht_sod=Sum('amount'))['bardasht_sod']
variz_sod_moarefi = transactions.filter(kind=5).aggregate(variz_sod_moarefi=Sum('amount'))['variz_sod_moarefi'] or 0
r = (seporde + variz_sod + variz_sod_moarefi) - (marjo + bardasht_sod)
print(f'{seporde}   {marjo}   {variz_sod}   {bardasht_sod}   {variz_sod_moarefi}')
print(m.mojodi_moarefishodeha_ta())

print(len(Transaction.objects.filter(profile__in=m.moarefi_shode_ha.all())))
