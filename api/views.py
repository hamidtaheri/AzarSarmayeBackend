import datetime

import jdatetime
import openpyxl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from graphene_django.views import GraphQLView

from api.models import Profile, mohasebe_sod_1_nafar, Transaction, ProfitCalculate, Pelekan, m2sh, \
    mohasebe_sod_moarefi_1_nafar
from backend import settings


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


def home(request):
    return render(request, 'home.html')


def mohasebe_sod_all_export_excel(az_date: datetime, ta_date: datetime):
    profit_excel = openpyxl.Workbook()
    profit_sheet = profit_excel.active
    profit_sheet.title = "sadid Sheet1"

    profit_sheet.cell(row=1, column=1, value="row num")
    profit_sheet.cell(row=1, column=2, value="id")
    profit_sheet.cell(row=1, column=3, value="name")
    profit_sheet.cell(row=1, column=4, value="amount")
    profit_sheet.cell(row=1, column=5, value="hesab")
    profit_sheet.cell(row=1, column=6, value="محاسبه شده توسط نرم افزار قدیمی")
    profit_sheet.cell(row=1, column=7, value="اختلاف")

    counter = detail_counter = 1
    for pr in Profile.objects.all():
        p: Profile = pr
        try:
            sod_list, sod_sum = mohasebe_sod_1_nafar(p.id, az_date, ta_date)

            counter += 1
            profit_sheet.cell(row=counter, column=1, value=counter - 1)
            profit_sheet.cell(row=counter, column=2, value=f"{p.id}")
            profit_sheet.cell(row=counter, column=3, value=f"{p.first_name} {p.last_name}")
            profit_sheet.cell(row=counter, column=4, value=sod_sum)
            profit_sheet.cell(row=counter, column=5, value=p.account_number)

            old_calculated_value = 0
            try:
                old_calculated: Transaction = Transaction.objects.filter(profile=pr, kind_id=3, effective_date=ta_date)[
                    0]
                old_calculated_value = old_calculated.amount
            except IndexError:
                pass

            profit_sheet.cell(row=counter, column=6, value=old_calculated_value)
            profit_sheet.cell(row=counter, column=7, value=sod_sum - old_calculated_value)



        except Pelekan.MultipleObjectsReturned:
            print(f'ERROR for {p}({p.id})  MultipleObjectsReturned')
            sod_sum = f'ERROR for {p}({p.id})  MultipleObjectsReturned'
        except Pelekan.DoesNotExist:
            print(f'ERROR for {p}({p.id})  DoesNotExist')
            sod_sum = f'ERROR for {p}({p.id})  DoesNotExist'
    filename = f"profit-{jdatetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    profit_excel.save(filename=f"{settings.MEDIA_ROOT}\\{filename}")
    print(f'finish')
    return f"{settings.MEDIA_URL}{filename}"


def mohasebe_sod_detail_all_export_excel(az_date: datetime, ta_date: datetime):
    profit_excel = openpyxl.Workbook()
    profit_sheet = profit_excel.active
    profit_sheet.title = "sadid Sheet1"

    profit_sheet.cell(row=1, column=1, value="row num")
    profit_sheet.cell(row=1, column=2, value="id")
    profit_sheet.cell(row=1, column=3, value="name")
    profit_sheet.cell(row=1, column=4, value="amount")
    profit_sheet.cell(row=1, column=5, value="hesab")
    profit_sheet.cell(row=1, column=6, value="محاسبه شده توسط نرم افزار قدیمی")
    profit_sheet.cell(row=1, column=7, value="اختلاف")

    profit_details_excel = openpyxl.Workbook()
    profit_details_sheet = profit_details_excel.active
    profit_details_sheet.title = "sadid Sheet1"

    profit_details_sheet.cell(row=1, column=1, value="row num")
    profit_details_sheet.cell(row=1, column=2, value="Profile_id")
    profit_details_sheet.cell(row=1, column=3, value="Profile_name")
    profit_details_sheet.cell(row=1, column=4, value="transaction_id")
    profit_details_sheet.cell(row=1, column=5, value="percent")
    profit_details_sheet.cell(row=1, column=6, value="amount")
    profit_details_sheet.cell(row=1, column=7, value="transaction_date")
    profit_details_sheet.cell(row=1, column=8, value="date_from")
    profit_details_sheet.cell(row=1, column=9, value="date_to")
    profit_details_sheet.cell(row=1, column=10, value="days")
    profit_details_sheet.cell(row=1, column=11, value="calculated_amount")
    profit_details_sheet.cell(row=1, column=12, value="تاریخ")

    counter = detail_counter = 1
    for pr in Profile.objects.all():
        p: Profile = pr
        try:
            sod_list, sod_sum = mohasebe_sod_1_nafar(p.id, az_date, ta_date)

            counter += 1
            profit_sheet.cell(row=counter, column=1, value=counter - 1)
            profit_sheet.cell(row=counter, column=2, value=f"{p.id}")
            profit_sheet.cell(row=counter, column=3, value=f"{p.first_name} {p.last_name}")
            profit_sheet.cell(row=counter, column=4, value=sod_sum)
            profit_sheet.cell(row=counter, column=5, value=p.account_number)

            old_calculated_value = 0
            try:
                old_calculated: Transaction = Transaction.objects.filter(profile=pr, kind_id=3, effective_date=ta_date)[
                    0]
                old_calculated_value = old_calculated.amount
            except IndexError:
                pass

            profit_sheet.cell(row=counter, column=6, value=old_calculated_value)
            profit_sheet.cell(row=counter, column=7, value=sod_sum - old_calculated_value)

            for pc in sod_list:
                detail_counter = detail_counter + 1
                pc: ProfitCalculate = pc
                profit_details_sheet.cell(row=detail_counter, column=1, value=detail_counter - 1)
                profit_details_sheet.cell(row=detail_counter, column=2, value=f"{pc.Profile.id}")
                profit_details_sheet.cell(row=detail_counter, column=3,
                                          value=f"{pc.Profile.first_name} {pc.Profile.last_name}")
                profit_details_sheet.cell(row=detail_counter, column=4, value=f"{pc.transaction.id}")
                profit_details_sheet.cell(row=detail_counter, column=5, value=f"{pc.percent}")
                profit_details_sheet.cell(row=detail_counter, column=6, value=pc.amount)
                profit_details_sheet.cell(row=detail_counter, column=7, value=f"{pc.transaction.effective_date}")
                profit_details_sheet.cell(row=detail_counter, column=8, value=f"{pc.date_from}")
                profit_details_sheet.cell(row=detail_counter, column=9, value=f"{pc.date_to}")
                profit_details_sheet.cell(row=detail_counter, column=10, value=f"{pc.days}")
                profit_details_sheet.cell(row=detail_counter, column=11, value=pc.calculated_amount)
                profit_details_sheet.cell(row=detail_counter, column=12, value=f"{m2sh(pc.transaction.effective_date)}")

        except Pelekan.MultipleObjectsReturned:
            print(f'ERROR for {p}({p.id})  MultipleObjectsReturned')
            sod_sum = f'ERROR for {p}({p.id})  MultipleObjectsReturned'
        except Pelekan.DoesNotExist:
            print(f'ERROR for {p}({p.id})  DoesNotExist')
            sod_sum = f'ERROR for {p}({p.id})  DoesNotExist'

    profit_excel.save(filename=f"profit-{jdatetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")
    profit_details_excel.save(filename=f"profit_details-{jdatetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")
    print(f'finish')


def mohasebe_sod_moarefi_all_export_excel(az_date: datetime, ta_date: datetime):
    profit_excel = openpyxl.Workbook()
    profit_sheet = profit_excel.active
    profit_sheet.title = "sadid Sheet1"

    profit_sheet.cell(row=1, column=1, value="row num")
    profit_sheet.cell(row=1, column=2, value="id")
    profit_sheet.cell(row=1, column=3, value="name")
    profit_sheet.cell(row=1, column=4, value="amount")
    profit_sheet.cell(row=1, column=5, value="hesab")
    profit_sheet.cell(row=1, column=6, value="محاسبه شده توسط نرم افزار قدیمی")
    profit_sheet.cell(row=1, column=7, value="اختلاف")

    profit_details_excel = openpyxl.Workbook()
    profit_details_sheet = profit_details_excel.active
    profit_details_sheet.title = "sadid Sheet1"

    profit_details_sheet.cell(row=1, column=1, value="row num")
    profit_details_sheet.cell(row=1, column=2, value="Profile_id")
    profit_details_sheet.cell(row=1, column=3, value="Profile_name")
    profit_details_sheet.cell(row=1, column=4, value="transaction_id")
    profit_details_sheet.cell(row=1, column=5, value="percent")
    profit_details_sheet.cell(row=1, column=6, value="amount")
    profit_details_sheet.cell(row=1, column=7, value="transaction_date")
    profit_details_sheet.cell(row=1, column=8, value="date_from")
    profit_details_sheet.cell(row=1, column=9, value="date_to")
    profit_details_sheet.cell(row=1, column=10, value="days")
    profit_details_sheet.cell(row=1, column=11, value="calculated_amount")
    profit_details_sheet.cell(row=1, column=12, value="تاریخ")
    profit_details_sheet.cell(row=1, column=13, value="name")

    counter = detail_counter = 1
    for pr in Profile.objects.all():
        p: Profile = pr
        try:
            sod_list, sod_sum = mohasebe_sod_moarefi_1_nafar(p.id, az_date, ta_date)

            counter += 1
            profit_sheet.cell(row=counter, column=1, value=counter - 1)
            profit_sheet.cell(row=counter, column=2, value=f"{p.id}")
            profit_sheet.cell(row=counter, column=3, value=f"{p.first_name} {p.last_name}")
            profit_sheet.cell(row=counter, column=4, value=f"{sod_sum}")
            profit_sheet.cell(row=counter, column=5, value=p.accountـnumber)
            old_calculated_value = 0
            try:
                old_calculated: Transaction = Transaction.objects.filter(profile=pr, kind_id=5,
                                                                         effective_date=ta_date).aggregate(
                    Sum('amount'))
                old_calculated_value = old_calculated['amount__sum'] or 0
            except IndexError:
                pass

            profit_sheet.cell(row=counter, column=6, value=old_calculated_value)
            profit_sheet.cell(row=counter, column=7, value=sod_sum - old_calculated_value)

            for pc in sod_list:
                detail_counter = detail_counter + 1
                pc: ProfitCalculate = pc
                profit_details_sheet.cell(row=detail_counter, column=1, value=detail_counter - 1)
                profit_details_sheet.cell(row=detail_counter, column=2, value=f"{pc.Profile.id}")
                profit_details_sheet.cell(row=detail_counter, column=3,
                                          value=f"{pc.Profile.first_name} {pc.Profile.last_name}")
                profit_details_sheet.cell(row=detail_counter, column=4, value=f"{pc.transaction.id}")
                profit_details_sheet.cell(row=detail_counter, column=5, value=f"{pc.percent}")
                profit_details_sheet.cell(row=detail_counter, column=6, value=f"{pc.amount}")
                profit_details_sheet.cell(row=detail_counter, column=7, value=f"{pc.transaction.effective_date}")
                profit_details_sheet.cell(row=detail_counter, column=8, value=f"{pc.date_from}")
                profit_details_sheet.cell(row=detail_counter, column=9, value=f"{pc.date_to}")
                profit_details_sheet.cell(row=detail_counter, column=10, value=f"{pc.days}")
                profit_details_sheet.cell(row=detail_counter, column=11, value=f"{pc.calculated_amount}")
                profit_details_sheet.cell(row=detail_counter, column=12, value=f"{m2sh(pc.transaction.effective_date)}")
                profit_details_sheet.cell(row=detail_counter, column=13,
                                          value=f"{pc.transaction.profile.first_name} {pc.transaction.profile.last_name}")

        except Pelekan.MultipleObjectsReturned:
            print(f'ERROR for {p}({p.id})  MultipleObjectsReturned')
            sod_sum = f'ERROR for {p}({p.id})  MultipleObjectsReturned'
        except Pelekan.DoesNotExist:
            print(f'ERROR for {p}({p.id})  DoesNotExist')
            sod_sum = f'ERROR for {p}({p.id})  DoesNotExist'

    profit_excel.save(filename=f"profit-moarefi-{jdatetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")
    profit_details_excel.save(
        filename=f"profit-moarefi_details-{jdatetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")
    print(f'finish')
