import datetime

import pytz
from django.test import TestCase
from api.models import Ashkhas, Tarakonesh, TransactionKind, sh2m, miladi_to_shamsi


class TarakoneshTestClass(TestCase):
    tk1 = TransactionKind.objects.get(id=1)
    a = Ashkhas(id=1, Fname='Morteza', Lname='Motahari')

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

        cls.a.save()
        # 
        # cls.tk1.save()
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

    def test_1_tarakonesh_1(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای اردیبهشت که ماه ۳۱ روزه است
        :return:
        """
        t = Tarakonesh(Mablagh=500000000, g_Tarikh_Moaser=sh2m("1400/01/01"),
                       date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), DarMelyoon=70000)
        t.kind = self.tk1
        t.shakhs = self.a
        t.save()
        self.a.tarakoneshha.add(t)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31"))
        self.assertEqual(len(lst), 1)
        print(s)
        self.assertEqual(s, 3616667)
        self.assertEqual(self.a.mojodi_ta(ta=datetime.date(2021, 0o5, 21)), 500000000)

    def test_1_tarakonesh_2(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای مهر که ماه ۳۰ روزه است
        :return:
        """
        t = Tarakonesh(Mablagh=500000000, g_Tarikh_Moaser=sh2m("1400/01/01"),
                       date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), DarMelyoon=70000)
        t.kind = self.tk1
        t.shakhs = self.a
        t.save()
        self.a.tarakoneshha.add(t)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/07/01"), ta_date=sh2m("1400/07/30")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/07/01"), ta_date=sh2m("1400/07/30"))
        self.assertEqual(len(lst), 1)
        print(s)
        self.assertEqual(s, 3500000)
        self.assertEqual(self.a.mojodi_ta(ta=datetime.date(2021, 0o5, 21)), 500000000)

    def test_1_tarakonesh_3(self):
        """
                محاسبه سود برای فردی که ابتدای سال مبلغ ۵۰ میلیون تومان و ۱۵ اردیبهشت ۱۰ میلیون تومان واریز کرده در بازه زمانی ابتدا تا انتهای مهر که ماه ۳۰ روزه است
        :return:
        """
        t1 = Tarakonesh(Mablagh=500000000, g_Tarikh_Moaser=sh2m("1400/01/01"),
                        date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), DarMelyoon=70000)

        t2 = Tarakonesh(Mablagh=100000000, g_Tarikh_Moaser=sh2m("1400/02/15"),
                        date_time=datetime.datetime(2021, 0o1, 0o1, 1, tzinfo=pytz.UTC), DarMelyoon=70000)
        t1.kind = self.tk1
        t1.shakhs = self.a
        t1.save()

        t2.kind = self.tk1
        t2.shakhs = self.a
        t2.save()
        self.a.tarakoneshha.add(t1)
        self.a.tarakoneshha.add(t2)
        print(self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31")))
        lst, s = self.a.mohasebe_sod_old(az_date=sh2m("1400/02/01"), ta_date=sh2m("1400/02/31"))
        self.assertEqual(len(lst), 2)
        print(s)
        self.assertEqual(s, 4013334)
        self.assertEqual(self.a.mojodi_ta(ta=sh2m("1400/02/31")), 600000000)

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
