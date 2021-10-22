# import api
import datetime

from django.utils.datetime_safe import strftime
from django.utils.timezone import now

from api.models import *
import openpyxl

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

mohasebe_sod_all(az_date, ta_date)

# mohasebe_sod_moarefi_all(az_date, ta_date)
# print(now())
# print(now().strftime('%y-%m-%d_%H-%M-%S'))


def days_after_transaction_start():
    for tr in Transaction.objects.filter(kind_id=1):
        tr: Transaction = tr
        tr_date = tr.effective_date
        now_date = now().date()
        diff = (now_date - tr_date).days
        print(f'{tr.Tarikh_Moaser} {tr.effective_date} {diff}')
