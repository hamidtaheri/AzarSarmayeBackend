import datetime

import api.models

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
m = api.models.Ashkhas.objects.get(id=2)
print(m)
az_date = datetime.date(year=2021, month=4, day=21)
ta_date = datetime.date(year=2021, month=5, day=21)
mo = m.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
print(len(mo))
summ = 0
for m1 in mo:
    summ = m1.calculated_amount + summ
    print(m1)

print(summ)
print('------')
az_date = datetime.date(year=2021, month=5, day=22)
ta_date = datetime.date(year=2021, month=6, day=21)
mo = m.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
print(len(mo))
summ = 0
for m1 in mo:
    summ = m1.calculated_amount + summ
    print(m1)

print(summ)
