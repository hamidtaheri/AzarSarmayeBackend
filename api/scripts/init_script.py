from django.utils.timezone import now

from api.models import *

# superuser: User = User(username='superadmin', is_superuser=True, is_staff=True)
# superuser.set_password('Admin123')
# superuser.save()
print(f'start:{now()}')
for p in Profile.objects.all():
    p.state = 'START'
    p.to_convert()
    p.save()
print(f'profile end:{now()}')

user1: User = User.objects.get(id=1)
for t in Transaction.objects.all():
    t.date = sh2m(t.tarikh)
    t.effective_date = sh2m(t.Tarikh_Moaser)
    t.presenter_effective_date = sh2m(t.Tarikh_Moaser_Moaref)
    t.state = 'START'
    t.to_convert()
    t.created_by = user1
    t.save()

print(f'transaction end:{now()}')
