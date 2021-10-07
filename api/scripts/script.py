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
