from api.models import *


def test1():
    tr = Transaction()
    tr.to_convert()
    tr.save()


test1()
