from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model


class User(AbstractUser):
    mobile = models.CharField('تلفن همراه', max_length=11, blank=True, null=True,help_text='شماره موبایل')

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    title = models.CharField('عنوان', max_length=100, blank=False, null=False)
    body = models.TextField('متن', blank=True, null=True)
    is_public = models.BooleanField('عمومی؟', default=True, )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.title}'


class Transaction(models.Model):
    Variz = 'Variz'
    Bardasht = 'Bardast'

    TRASACTION_TYPE = [
        (Variz, "واریز"),
        (Bardasht, "برداشت"),
    ]

    user = models.ForeignKey(get_user_model(), verbose_name='کاربر', on_delete=models.DO_NOTHING,
                             related_name='transactions', blank=False, null=False)
    # j_date = jmodels.jDateField(verbose_name='تاریخ', blank=False, null=False)
    j_date = models.DateField(verbose_name='تاریخ', blank=False, null=False)
    amount = models.PositiveBigIntegerField(verbose_name='مبلغ', blank=False, null=False)
    type = models.CharField(verbose_name='نوع', choices=TRASACTION_TYPE, max_length=7)

    # logging fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                   related_name='create_by', editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=False, null=False,
                                    related_name='modified_by', editable=False)

    class Meta:
        verbose_name = "عملیات مالی(واریز/برداشت)"
        verbose_name_plural = "عملیات مالی(واریز/برداشت)"

        permissions = (
            ("can_add_transaction_for_self", "میتواند برای خودش تراکنش ثبت کند"),
            ("can_add_transaction_for_all", "میتواند برای دیگران تراکنش ثبت کند"),
            ("can_view_transaction_for_all", "میتواند تراکنش دیگران را مشاهده کند"),
        )

    def __str__(self):
        return f'{self.type} {self.amount} {self.user} {self.j_date}'

    def save(self, *args, **kwargs):
        print(f'save {self.user} {self.type} {self.amount}')

        current_user: User = get_current_user()
        # کاربر وارد نشده
        if (not current_user.is_authenticated) or current_user.is_anonymous or current_user is None:
            raise PermissionDenied()
        if not current_user.has_perm('can_add_transaction_for_all'):  # کابر جاری مجاز نیست برای دیگران تراکنش ثبت کند
            self.user = current_user
        if not self.pk:
            self.created_by = current_user
        self.modified_by = current_user
        # super(Transaction, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
