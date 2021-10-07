import datetime

import pytz
from django.test import TestCase

import api.models
from api.models import Profile, Transaction, TransactionKind, sh2m, miladi_to_shamsi


class TarakoneshTestClass(TestCase):
    tk1 = TransactionKind.objects.get(id=1)
    a = Profile(id=1, first_name='Morteza', last_name='Motahari')
    user = api.models.User()
    user.username = "user"

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

        cls.a.save()
        # 
        cls.tk1.save()
        cls.user.save()
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    # def test_false_is_true(self):
    #     print("Method: test_false_is_true.")
    #     self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def test_1_tarakonesh_ordibehest_31(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای اردیبهشت که ماه ۳۱ روزه است
        :return:
        """
        t = Transaction(amount=500000000, effective_date=sh2m("1400/01/01"),
                        date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)
        t.kind = self.tk1
        t.profile = self.a
        t.created_by = self.user
        t.modified_by = self.user
        t.save()
        self.a.transactions.add(t)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31"))
        self.assertEqual(len(lst), 1)
        print(s)
        self.assertEqual(s, 3616667)
        self.assertEqual(self.a.mojodi_ta(ta=datetime.date(2021, 0o5, 21)), 500000000)

    def test_1_tarakonesh_ordibehest_30(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا 30 اردیبهشت که ماه ۳۱ روزه است
        :return:
        """
        t = Transaction(amount=500000000, effective_date=sh2m("1400/01/01"),
                        date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)
        t.kind = self.tk1
        t.profile = self.a
        t.created_by = self.user
        t.modified_by = self.user
        t.save()
        self.a.transactions.add(t)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/30")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/30"))
        self.assertEqual(len(lst), 1)
        print(s)
        self.assertEqual(s, 3500000)  # 3616667
        self.assertEqual(self.a.mojodi_ta(ta=datetime.date(2021, 0o5, 21)), 500000000)

    def test_1_tarakonesh_mehr_30(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای مهر که ماه ۳۰ روزه است
        :return:
        """
        t = Transaction(amount=500000000, effective_date=sh2m("1400/01/01"),
                        date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)
        t.kind = self.tk1
        t.profile = self.a
        t.created_by = self.user
        t.modified_by = self.user
        t.save()
        self.a.transactions.add(t)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/07/01"), ta_date=sh2m("1400/07/30")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/07/01"), ta_date=sh2m("1400/07/30"))
        self.assertEqual(len(lst), 1)
        print(s)
        self.assertEqual(s, 3500000)
        self.assertEqual(self.a.mojodi_ta(ta=datetime.date(2021, 0o5, 21)), 500000000)

    def test_2_tarakonesh_ordibehest_31(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان و ۱۵ اردیبهشت ۱۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای مهر که ماه ۳۰ روزه است
        :return:
        """
        t1 = Transaction(amount=500000000, effective_date=sh2m("1400/01/01"),
                         date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)

        t2 = Transaction(amount=100000000, effective_date=sh2m("1400/02/15"),
                         date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)
        t1.kind = self.tk1
        t1.profile = self.a
        t1.created_by = self.user
        t1.modified_by = self.user
        t1.save()

        t2.kind = self.tk1
        t2.profile = self.a
        t2.created_by = self.user
        t2.modified_by = self.user
        t2.save()
        self.a.transactions.add(t1)
        self.a.transactions.add(t2)
        # print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31"))
        for l in lst:
            print(l)
        self.assertEqual(len(lst), 2)
        print(s)
        self.assertEqual(s, 4013334)
        self.assertEqual(self.a.mojodi_ta(ta=sh2m("1400/02/31")), 600000000)

    def test_2_tarakonesh_ordibehest_30(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان و ۱۵ اردیبهشت ۱۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای مهر که ماه ۳۰ روزه است
        :return:
        """
        t1 = Transaction(amount=500000000, effective_date=sh2m("1400/01/01"),
                         date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)

        t2 = Transaction(amount=100000000, effective_date=sh2m("1400/02/15"),
                         date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), percent=70000)
        t1.kind = self.tk1
        t1.profile = self.a
        t1.created_by = self.user
        t1.modified_by = self.user
        t1.save()

        t2.kind = self.tk1
        t2.profile = self.a
        t2.created_by = self.user
        t2.modified_by = self.user
        t2.save()
        self.a.transactions.add(t1)
        self.a.transactions.add(t2)
        # print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/30"))
        for l in lst:
            print(l)
        self.assertEqual(len(lst), 2)
        print(s)
        self.assertEqual(s, 3873333)
        self.assertEqual(self.a.mojodi_ta(ta=sh2m("1400/02/30")), 600000000)

    def test_shamsi_to_miladi_1(self):
        shamsi = "1400/07/05"
        miladi: datetime.date = sh2m(shamsi)
        self.assertEqual(datetime.date(2021, 9, 27), miladi)

    def test_shamsi_to_miladi_2(self):
        shamsi = "1361/10/03"
        miladi: datetime.date = sh2m(shamsi)
        self.assertEqual(datetime.date(1982, 12, 24), miladi)

    def test_shamsi_to_miladi_3(self):
        shamsi = "1410/06/01"
        miladi: datetime.date = sh2m(shamsi)
        self.assertEqual(datetime.date(2031, 8, 23), miladi)

    def test_shamsi_to_miladi_4(self):
        shamsi = "1440/2/1"
        miladi: datetime.date = sh2m(shamsi)
        self.assertEqual(datetime.date(2061, 4, 20), miladi)

    def test_miladi_to_shamsi_1(self):
        miladi = datetime.date(2021, 12, 1)
        print(miladi_to_shamsi(miladi))
        self.assertEqual("1400-09-10", miladi_to_shamsi(miladi))
