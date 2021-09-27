import datetime

import jdatetime

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
mo, so = m.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
print(len(mo))
print(mo)
print(so)


def shamsi_to_miladi(j_date: str) -> datetime.date:
    """
    تبدیل تاریخ شمسی به میلادی
    :param j_date: رشته تاریخ شمسی مانند ۱۴۰۰/۱۰/۰۳
    :return: datetime.date تاریخ میلادی
    """
    jyear = int(float(j_date[0:4]))
    jmonth = int(float(j_date[5:7]))
    jday = int(float(j_date[8:10]))
    (gyear, gmonth, gday) = jdatetime.JalaliToGregorian(jyear=jyear, jmonth=jmonth,
                                                        jday=jday).getGregorianList()
    return datetime.date(gyear, gmonth, gday)


shamsi_date = "1400/07/05"
print(shamsi_to_miladi(shamsi_date))
