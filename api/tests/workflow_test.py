import datetime

import pytz
from django.test import TestCase

import api.models
from api.models import Profile, Transaction, TransactionKind, sh2m, miladi_to_shamsi, Pelekan


class WorkflowTestClass(TestCase):
    fixtures = ['dump-1400-08-01.json', ]
    a = Profile(id=1, first_name='Morteza', last_name='Motahari')
    user = api.models.User()
    user.username = "user"

    # user = api.models.User.objects.get(id=2)
    # fixtures = ['/api/fixtures/dump-1400-07-20.json', ]  # No fixture named 'dump-1400-07-20' found.

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        cls.tk1 = TransactionKind.objects.get(id=1)

        cls.a.save()
        # #
        # cls.tk1.save()
        # cls.user.save()
        cls.user = api.models.User.objects.get(id=1)
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass