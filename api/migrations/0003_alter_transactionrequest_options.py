# Generated by Django 3.2.9 on 2021-12-15 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211215_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionrequest',
            options={'permissions': (('view_all_TransactionRequests', 'مشاهده همه درخواست های مربوط به تراکنش ها'), ('add_TransactionRequests_for_others', 'ایجاد درخواست مربوط به تراکنش برای دیگران'))},
        ),
    ]
