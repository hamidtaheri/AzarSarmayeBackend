from api.models import *

# superuser: User = User(username='superadmin', is_superuser=True, is_staff=True)
# superuser.set_password('Admin123')
# superuser.save()
for t in Transaction.objects.all():
    t.date = sh2m(t.tarikh)
    t.effective_date = sh2m(t.Tarikh_Moaser)
    t.presenter_effective_date = sh2m(t.Tarikh_Moaser_Moaref)
    t.save()
