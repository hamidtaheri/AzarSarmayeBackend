import datetime

import jdatetime
from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet, Sum
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model


class MyException(Exception):
    pass


day_in_month = 30


class User(AbstractUser):
    mobile = models.CharField('تلفن همراه', max_length=11, blank=True, null=True, help_text='شماره موبایل')

    def __str__(self):
        return f'{self.username}'


class TransactionKind(models.Model):
    title = models.CharField(verbose_name='نوع تراکنش', max_length=30)
    description = models.TextField(verbose_name='توضیح')

    def __str__(self):
        return f'{self.id}-{self.title}'


class Transaction_old(models.Model):
    charge = 'charge'
    withdraw = 'withdraw'
    withdraw_profit = 'withdraw_profit'

    TRASACTION_KINDS = [
        (charge, "واریز"),
        (withdraw, "برداشت"),
        (withdraw_profit, "برداشت سود"),
    ]

    user = models.ForeignKey(get_user_model(), verbose_name='کاربر', on_delete=models.DO_NOTHING,
                             related_name='transactions', blank=False, null=False)
    # date = jmodels.jDateField(verbose_name='تاریخ', blank=False, null=False)
    date = models.DateField(verbose_name='تاریخ', blank=False, null=False)
    amount = models.PositiveBigIntegerField(verbose_name='مبلغ', blank=False, null=False)
    kind = models.ForeignKey(TransactionKind, verbose_name='نوع', on_delete=models.CASCADE)

    @property
    def shamse_date(self):
        return jdatetime.date.fromgregorian(date=self.date).strftime(format="%Y-%m-%d")

    class Meta:
        verbose_name = "عملیات مالی(واریز/برداشت)"
        verbose_name_plural = "عملیات مالی(واریز/برداشت)"

        permissions = (
            ("can_add_transaction_for_self", "میتواند برای خودش تراکنش ثبت کند"),
            ("can_add_transaction_for_all", "میتواند برای دیگران تراکنش ثبت کند"),
            ("can_view_transaction_for_all", "میتواند تراکنش دیگران را مشاهده کند"),
        )

    def __str__(self):
        return f'{self.kind} {self.amount} {self.user} {self.date}'

    def before_save_transaction(self):
        current_user: User = get_current_user()
        # کاربر وارد نشده
        if (not current_user.is_authenticated) or current_user.is_anonymous or current_user is None:
            raise PermissionDenied()
        if not current_user.has_perm('can_add_transaction_for_all'):  # کابر جاری مجاز نیست برای دیگران تراکنش ثبت کند
            if self.user != current_user:
                raise PermissionDenied()
        if not self.pk:
            self.created_by = current_user
        self.modified_by = current_user

        print(self)

    def save(self, *args, **kwargs):
        print(f'save {self.user} {self.kind} {self.amount}')

        self.before_save_transaction()

        profit_calculate_objects_for_user: QuerySet[ProfitCalculate] = ProfitCalculate.objects.filter(user=self.user)
        # قبلا در جدول محاسبه سود برای این کاربر رکوردی ثبت نشده است
        new_profit_calculate: ProfitCalculate = ProfitCalculate()
        if profit_calculate_objects_for_user.count() == 0 or profit_calculate_objects_for_user is None:
            new_profit_calculate.user = self.user
            new_profit_calculate.date_from = self.date
            new_profit_calculate.amount = self.amount

            super().save(*args, **kwargs)

            new_profit_calculate.transaction = self
            new_profit_calculate.save()
            # اولین رکورد در جدول محاسبه سود برای این کاربر ثبت شد

        else:
            # به روز رسانی آخرین رکورد جدول محاسبه سود و ایجاد رکورد جدید
            profit_calculate_for_user_latest_by_created = profit_calculate_objects_for_user.latest('created')
            profit_calculate_for_user_latest_by_id = profit_calculate_objects_for_user.latest('id')
            profit_calculate_for_user_latest_date_to = profit_calculate_objects_for_user.filter(
                date_to__isnull=True)
            if profit_calculate_for_user_latest_date_to.count() == 1 and \
                    profit_calculate_for_user_latest_by_created == profit_calculate_for_user_latest_by_id and \
                    profit_calculate_for_user_latest_by_id == profit_calculate_for_user_latest_date_to[0]:
                latest_profit_calculate: ProfitCalculate = profit_calculate_for_user_latest_by_created
                latest_profit_calculate.date_to = self.date
                days = (self.date - latest_profit_calculate.date_from).days
                if days < 0:
                    raise MyException(
                        f'new transaction date ({self.date}) must newest from last transaction ({latest_profit_calculate.date_from})')
                latest_profit_calculate.days = days
                latest_profit_calculate.save()

                new_profit_calculate.user = self.user
                new_profit_calculate.date_from = self.date
                new_amount = 0
                if self.type == 'withdraw':  # برداشت از حساب
                    new_amount = latest_profit_calculate.amount - self.amount
                elif self.type == 'charge':  # واریز به حساب
                    new_amount = latest_profit_calculate.amount + self.amount

                new_profit_calculate.amount = new_amount

                super().save(*args, **kwargs)

                new_profit_calculate.transaction = self
                new_profit_calculate.save()

            print(f'ProfitCalculate  availebale for user:{self.user}')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True, )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    code_meli = models.CharField(max_length=10, blank=True, null=True)
    adress = models.CharField(max_length=500, blank=True, null=True)
    shomare_kart = models.CharField(max_length=100, blank=True, null=True)
    shomare_hesab = models.CharField(max_length=100, blank=True, null=True)
    presenter = models.ForeignKey('self', verbose_name='معرف', blank=True, null=True,
                                  on_delete=models.CASCADE, related_name='+')  # moarefi_shode_ha
    percent = models.IntegerField(blank=True, null=True)
    presenter_percent = models.IntegerField(blank=True, null=True)
    get_profit = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    charge_to_presenter = models.BooleanField(blank=True, null=True)
    self_presenter = models.BooleanField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    presenter_2 = models.IntegerField(blank=True, null=True)
    presenter_percent_2 = models.IntegerField(blank=True, null=True)
    self_presenter_2 = models.BooleanField(blank=True, null=True)

    def tarakonesh_sum_ta(self, kind: int, ta: datetime = None, ) -> float:
        if ta:
            tr = Transaction.objects.filter(profile=self, kind=kind, effective_date__lte=ta).aggregate(
                Sum('amount'))
        else:
            tr = Transaction.objects.filter(profile=self, kind=kind).aggregate(Sum('amount'))
        try:
            r = tr['amount__sum']
            if r is None:
                r = 0
        except IndexError:
            r = 0
        return r

    def mojodi_ta(self, ta: datetime.date = None) -> float:
        """
        موجودی حساب یعنی مجموع سرمایه گزاری ها و سودها منهای برداشت سود و مرجوعی
        :param ta:  تا تاریخ اگر تاریخ
        :return:  موجودی
        """
        if ta is None:
            ta = datetime.date.today()

        seporde = self.tarakonesh_sum_ta(kind=1, ta=ta)  # سپرده گذاری
        marjo = self.tarakonesh_sum_ta(kind=2, ta=ta)  # مرجوع
        variz_sod = self.tarakonesh_sum_ta(kind=3, ta=ta)  # واریز سود
        bardasht_sod = self.tarakonesh_sum_ta(kind=4, ta=ta)  # برداشت سود
        variz_sod_moarefi = self.tarakonesh_sum_ta(kind=5, ta=ta)  # واریز سود معرفی
        r = (seporde + variz_sod + variz_sod_moarefi) - (marjo + bardasht_sod)
        return r

    def mohasebe_sod_old(self, az_date: datetime.date, ta_date: datetime.date):
        """
        محاسبه سود بر اساس اینکه هر واریزی درصد سود خود را دارد
        :param user:
        :param az_date:
        :param ta_date:
        :return:لیست محاسبات سود و مجموع انها را بر میگرداند
        """
        sum_of_sod = 0
        # واریزی های کاربر تا پیش از تاریخ پایان

        mohasebat_sod: list[ProfitCalculate] = list[ProfitCalculate]()
        tarakoneshs: QuerySet[Transaction] = Transaction.objects.filter(profile=self,
                                                                        effective_date__lte=ta_date,
                                                                        kind_id=1)
        for tr in tarakoneshs:
            mohasebe_sod: ProfitCalculate = tr.profit_calculator(az_date=az_date, ta_date=ta_date)
            sum_of_sod = sum_of_sod + mohasebe_sod.calculated_amount
            mohasebat_sod.append(mohasebe_sod)

        return mohasebat_sod, sum_of_sod

    def __str__(self):
        return f'{self.first_name}   {self.last_name}'


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tarakoneshha')
    tarikh = models.CharField(max_length=10)
    date = models.DateField(null=True, blank=True, )
    Tarikh_Moaser = models.CharField(max_length=10)
    effective_date = models.DateField(null=True, blank=True)
    Tarikh_Moaser_Moaref = models.CharField(max_length=10)
    presenter_effective_date = models.DateField(null=True, blank=True)
    date_time = models.DateTimeField()
    amount = models.BigIntegerField()
    kind = models.ForeignKey(TransactionKind, on_delete=models.CASCADE, related_name='tarakoneshha')
    NahveyePardakht = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    Tbl_Pardakht_List_id = models.IntegerField(blank=True, null=True)
    percent = models.IntegerField()

    # logging fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                   related_name='create_by', editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                    related_name='modified_by', editable=False)

    def __str__(self):
        return f'{self.id} {self.profile.last_name}'

    class Meta:
        ordering = ['effective_date']

    def percent_calculator(self) -> float:
        if self.effective_date < datetime.date(2021, 0o6, 22):  # 1400/04/01
            return self.percent
        else:
            mojodi = self.profile.mojodi_ta(ta=self.effective_date)
            dar_melyon = Pelekan.objects.get(az__lte=mojodi, ta__gte=mojodi).percent
            return dar_melyon

    def profit_calculator(self, az_date: datetime.date, ta_date: datetime.date):
        start_date: datetime.date = az_date
        end_date: datetime.date = ta_date  # اگر بخشی از این واریزی پیش از پایان دوره مرجوع گردد سود تعداد روز شامل را دریافت میکند نه تا پایان دوره را. این فرض در حال حاظر ممکن نیست
        if self.effective_date > az_date:
            start_date = self.effective_date  # این واریزی در بین دوره محاسبه سود انجام شده نه از پیش از آن بنابراین سود معادل تعداد روز شامل را در یافت میکند

        # sod = tr.percent  # نحوه محاسبه سود؟؟؟؟؟؟؟؟ اینجاست
        sod = self.percent_calculator()  # نحوه محاسبه سود؟؟؟؟؟؟؟؟ اینجاست
        mohasebe_sod: ProfitCalculate = ProfitCalculate()
        mohasebe_sod.user = self.profile.user
        mohasebe_sod.date_from = start_date
        mohasebe_sod.date_to = end_date
        mohasebe_sod.days = (end_date - start_date).days + 1  # فاصله روز شروع تا پایان +۱ شد
        mohasebe_sod.amount = self.amount
        mohasebe_sod.percent = sod
        mohasebe_sod.calculated_amount = round(self.amount * (sod / 10000000) * (mohasebe_sod.days / day_in_month), 0)
        return mohasebe_sod


class ProfitCalculate(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='کاربر', on_delete=models.DO_NOTHING,
                             related_name='ProfitCalculates', blank=False, null=False)
    date_from = models.DateField(verbose_name='از تاریخ', blank=False, null=False)
    date_to = models.DateField(verbose_name='تا تاریخ', blank=True, null=True)
    days = models.PositiveIntegerField(verbose_name='تعداد روز', blank=True, null=True)
    amount = models.PositiveBigIntegerField(verbose_name='مبلغ', blank=True, null=True)
    percent = models.IntegerField(verbose_name='درصد', validators=[MinValueValidator(1), MaxValueValidator(10)],
                                  blank=True, null=True)
    # تراکنشی که این رکورد بر اساس آن ساخته شده
    transaction = models.OneToOneField(to=Transaction, verbose_name='تراکنش متناظر', blank=False, null=False,
                                       on_delete=models.DO_NOTHING,
                                       related_name='ProfitCalculate')
    calculated_amount = models.PositiveIntegerField(verbose_name='مبلغ سود محاسبه شده', null=True, blank=True)
    balance = models.BooleanField(verbose_name='تسویه شده است', default=False)
    # تراکنشی که باغث شده این رکورد سود محاسبه شده تسویه گردد
    transaction_balance = models.ForeignKey(to=Transaction, verbose_name='تسویه شده با تراکنش',
                                            related_name='ProfitCalculates', on_delete=models.DO_NOTHING, null=True,
                                            blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f' from:({self.date_from} = {miladi_to_shamsi(self.date_from)}) to:({self.date_to} = {miladi_to_shamsi(self.date_to)}) days: ({self.days}) ' \
               f'amount: ({self.amount})  percent: ({self.percent}) final: ({self.calculated_amount})'


class Pelekan(models.Model):
    az = models.PositiveBigIntegerField()
    ta = models.PositiveBigIntegerField()
    percent = models.IntegerField()

    def __str__(self):
        return f'{self.az} --- {self.ta}  :  {self.percent}'


class Post(models.Model):
    title = models.CharField('عنوان', max_length=100, blank=False, null=False)
    body = models.TextField('متن', blank=True, null=True)
    is_public = models.BooleanField('عمومی؟', default=True, )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.title}'


def shamsi_to_miladi(j_date: str, sep: str = "/") -> datetime.date:
    """
    تبدیل تاریخ شمسی به میلادی
    :param j_date: رشته تاریخ شمسی مانند ۱۴۰۰/۱۰/۰۳
    :param sep: جدا کننده تاریخ. پیشفرض / است
    :return: datetime.date تاریخ میلادی
    """
    shamsi = j_date.split(sep=sep)
    jyear = int(float(shamsi[0]))
    jmonth = int(float(shamsi[1]))
    jday = int(float(shamsi[2]))
    # jyear = int(float(j_date[0:4]))
    # jmonth = int(float(j_date[5:7]))
    # jday = int(float(j_date[8:10]))
    (gyear, gmonth, gday) = jdatetime.JalaliToGregorian(jyear=jyear, jmonth=jmonth,
                                                        jday=jday).getGregorianList()
    return datetime.date(gyear, gmonth, gday)


def sh2m(j_date: str, sep: str = "/") -> datetime.date:
    """
    تبدیل تاریخ شمسی به میلادی
    :param j_date: رشته تاریخ شمسی مانند ۱۴۰۰/۱۰/۰۳
    :param sep: جدا کننده تاریخ. پیشفرض / است
    :return: datetime.date تاریخ میلادی
    """
    return shamsi_to_miladi(j_date, sep)


def miladi_to_shamsi(g_date: datetime.date) -> str:
    return jdatetime.date.fromgregorian(date=g_date).strftime(format="%Y-%m-%d")


def m2sh(g_date: datetime.date) -> str:
    return miladi_to_shamsi(g_date)
