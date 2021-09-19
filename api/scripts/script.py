import datetime

import api.models

m = api.models.Ashkhas.objects.get(id=266)
print(m)
az_date = datetime.date(year=2021, month=4, day=21)  # 1400/01/31
ta_date = datetime.date(year=2021, month=5, day=21)  # 1400/02/31
mo = m.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
print(len(mo))
summ = 0
for m1 in mo:
    summ = m1.calculated_amount + summ
    print(m1)

print(summ)


