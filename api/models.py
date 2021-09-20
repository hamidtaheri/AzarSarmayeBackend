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


class User(AbstractUser):
    mobile = models.CharField('تلفن همراه', max_length=11, blank=True, null=True, help_text='شماره موبایل')

    def __str__(self):
        return f'{self.username}'


class TransactionKind(models.Model):
    title = models.CharField(verbose_name='نوع تراکنش', max_length=30)
    description = models.TextField(verbose_name='توضیح')

    def __str__(self):
        return f'{self.id}-{self.title}'


class Transaction(models.Model):
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

    # logging fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                   related_name='create_by', editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                    related_name='modified_by', editable=False)

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
        return f' from date: ({self.date_from}) to date: ({self.date_to}) days: ({self.days}) ' \
               f'amount: ({self.amount})  percent: ({self.percent}) final: ({self.calculated_amount})'


class Ashkhas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shakhs', blank=True, null=True, )
    Fname = models.CharField(max_length=100, blank=True, null=True)
    Lname = models.CharField(max_length=100, blank=True, null=True)
    CodeMeli = models.CharField(max_length=10, blank=True, null=True)
    Adress = models.CharField(max_length=500, blank=True, null=True)
    ShomareKart = models.CharField(max_length=100, blank=True, null=True)
    Hesab = models.CharField(max_length=100, blank=True, null=True)
    Moaref_Tbl_Ashkhas_id = models.ForeignKey('self', verbose_name='معرف', blank=True, null=True,
                                              on_delete=models.CASCADE, related_name='+')  # moarefi_shode_ha
    Mizan_Har_Melyoon = models.IntegerField(blank=True, null=True)
    Mizan_Har_Melyoon_Moaref = models.IntegerField(blank=True, null=True)
    Daryaft_Sood = models.BooleanField(blank=True, null=True)
    Des = models.CharField(max_length=100, blank=True, null=True)
    VarizBeMoaref = models.BooleanField(blank=True, null=True)
    MorefiBekhod = models.BooleanField(blank=True, null=True)
    Tel = models.CharField(max_length=20, blank=True, null=True)
    Moaref_Tbl_Ashkhas_id2 = models.IntegerField(blank=True, null=True)
    Mizan_Har_Melyoon_Moaref2 = models.IntegerField(blank=True, null=True)
    MorefiBekhod2 = models.BooleanField(blank=True, null=True)

    def tarakonesh_sum_ta(self, kind: int, ta: datetime = None, ) -> float:
        if ta:
            tr = Tarakonesh.objects.filter(shakhs=self, kind=kind, g_Tarikh_Moaser__lte=ta).aggregate(
                Sum('Mablagh'))
        else:
            tr = Tarakonesh.objects.filter(shakhs=self, kind=kind).aggregate(Sum('Mablagh'))
        try:
            r = tr['Mablagh__sum']
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

    def mohasebe_sod_old(self, az_date: datetime.date, ta_date: datetime.date) -> (list[ProfitCalculate], float):
        """
        محاسبه سود بر اساس اینکه هر واریزی درصد سود خود را دارد
        :param user:
        :param az_date:
        :param ta_date:
        :return:لیست محاسبات سود و مجموع انها را بر میگرداند
        """
        sum_of_sod = 0
        # واریزی های کاربر تا پیش از تاریخ پایان
        day_in_month = 30
        mohasebat_sod: list[ProfitCalculate] = list[ProfitCalculate]()
        tarakoneshs: QuerySet[Tarakonesh] = Tarakonesh.objects.filter(shakhs=self, g_Tarikh_Moaser__lte=ta_date,
                                                                      kind_id=1)
        for tr in tarakoneshs:
            mohasebe_sod: ProfitCalculate = ProfitCalculate()
            start_date: datetime.date = az_date
            end_date: datetime.date = ta_date  # اگر بخشی از این واریزی پیش از پایان دوره مرجوع گردد سود تعداد روز شامل را دریافت میکند نه تا پایان دوره را. این فرض در حال حاظر ممکن نیست
            if tr.g_Tarikh_Moaser > az_date:
                start_date = tr.g_Tarikh_Moaser  # این واریزی در بین دوره محاسبه سود انجام شده نه از پیش از آن بنابراین سود معادل تعداد روز شامل را در یافت میکند

            # sod = tr.DarMelyoon  # نحوه محاسبه سود؟؟؟؟؟؟؟؟ اینجاست
            sod = sod_calculator(tr)  # نحوه محاسبه سود؟؟؟؟؟؟؟؟ اینجاست

            mohasebe_sod.user = self.user
            mohasebe_sod.date_from = start_date
            mohasebe_sod.date_to = end_date
            mohasebe_sod.days = (end_date - start_date).days + 1  # فاصله روز شروع تا پایان +۱ شد
            mohasebe_sod.amount = tr.Mablagh
            mohasebe_sod.percent = sod
            mohasebe_sod.calculated_amount = tr.Mablagh * (sod / 10000000) * (mohasebe_sod.days / day_in_month)
            sum_of_sod = sum_of_sod + mohasebe_sod.calculated_amount
            mohasebat_sod.append(mohasebe_sod)

        return mohasebat_sod, sum_of_sod

    def __str__(self):
        return f'{self.Fname}   {self.Lname}'


class Tarakonesh(models.Model):
    shakhs = models.ForeignKey(Ashkhas, on_delete=models.CASCADE, related_name='tarakoneshha')
    tarikh = models.CharField(max_length=10)
    g_tarikh = models.DateField(null=True, blank=True, )
    Tarikh_Moaser = models.CharField(max_length=10)
    g_Tarikh_Moaser = models.DateField(null=True, blank=True)
    Tarikh_Moaser_Moaref = models.CharField(max_length=10)
    g_Tarikh_Moaser_Moaref = models.DateField(null=True, blank=True)
    date_time = models.DateTimeField()
    Mablagh = models.BigIntegerField()
    kind = models.ForeignKey(TransactionKind, on_delete=models.CASCADE, related_name='tarakoneshha')
    NahveyePardakht = models.CharField(max_length=40, blank=True, null=True)
    Des = models.CharField(max_length=100, blank=True, null=True)
    Tbl_Pardakht_List_id = models.IntegerField(blank=True, null=True)
    DarMelyoon = models.IntegerField()

    def __str__(self):
        return f'{self.id} {self.shakhs.Lname}'

    class Meta:
        ordering = ['g_Tarikh_Moaser']


class Pelekan(models.Model):
    az = models.PositiveBigIntegerField()
    ta = models.PositiveBigIntegerField()
    dar_melyoon = models.IntegerField()

    def __str__(self):
        return f'{self.az} --- {self.ta}  :  {self.dar_melyoon}'


def sod_calculator(tr: Tarakonesh) -> float:
    if tr.g_Tarikh_Moaser < datetime.date(2021, 0o6, 22):  # 1400/04/01
        return tr.DarMelyoon
    else:
        mojodi = tr.shakhs.mojodi_ta(ta=tr.g_Tarikh_Moaser)
        dar_melyon = Pelekan.objects.get(az__lte=mojodi, ta__gte=mojodi).dar_melyoon
        return dar_melyon


class Post(models.Model):
    title = models.CharField('عنوان', max_length=100, blank=False, null=False)
    body = models.TextField('متن', blank=True, null=True)
    is_public = models.BooleanField('عمومی؟', default=True, )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.title}'


def tarikh_to_g(j_date: str) -> datetime.date:
    jyear = int(float(j_date[0:4]))
    jmonth = int(float(j_date[5:7]))
    jday = int(float(j_date[8:10]))
    (gyear, gmonth, gday) = jdatetime.JalaliToGregorian(jyear=jyear, jmonth=jmonth,
                                                        jday=jday).getGregorianList()
    return datetime.datetime(gyear, gmonth, gday)
