from api.models import *


def test1():
    tr = Transaction()
    tr.to_convert()
    tr.save()


def transaction_state_to_converted(instance: Transaction):
    instance.to_convert()
    instance.save()


def transaction_state_to_to_stuff_add(instance: Transaction):
    instance.to_stuff_add()
    instance.save()


def transaction_state_converted_to_stuff_add_to_to_stuff_add(instance: Transaction):
    instance.converted_to_stuff_add()
    instance.save()


def new_transaction():
    tr = Transaction()
    tr.date_time = datetime.datetime.now()
    profile = Profile.objects.get(id=2)
    tr.profile = profile
    tr.amount = 112233
    tr.kind = TransactionKind.objects.get(id=1)
    tr.percent = 2000
    tr.created_by = User.objects.get(id=1)
    # tr.to_convert()

    tr.save()
    print(tr.id)


new_transaction()
# tr = Transaction.objects.get(id=141600)
# transaction_state_converted_to_stuff_add_to_to_stuff_add(tr)
# transaction_state_to_converted(tr)
