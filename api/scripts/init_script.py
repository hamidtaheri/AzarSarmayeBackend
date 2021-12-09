from django.utils.timezone import now

from api.models import *

# superuser: User = User(username='superadmin', is_superuser=True, is_staff=True)
# superuser.set_password('Admin123')
# superuser.save()
print(f'start:{now()}')
for p in Profile.objects.all():
    p.state = 'start'
    p.to_convert()
    p.save()
print(f'profile end:{now()}')

user1: User = User.objects.get(username='superadmin')
for t in Transaction.objects.all():
    t.date = sh2m(t.tarikh)
    t.effective_date = sh2m(t.Tarikh_Moaser)
    t.presenter_effective_date = sh2m(t.Tarikh_Moaser_Moaref)
    t.state = 'start'
    t.to_convert()
    t.created_by = user1
    t.created = now()
    t.save()

print(f'transaction end:{now()}')
