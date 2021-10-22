from django.db.models import QuerySet

from api.models import Profile

# همه
all_ashkhas:QuerySet[Profile] = Profile.objects.all()

# معرفی شده ها
moarefi_shode_ha: QuerySet[Profile] = all_ashkhas.filter(presenter__isnull=False).order_by('presenter')

# معرفی نشده ها
moarefi_na_shode_ha = all_ashkhas.filter(presenter__isnull=True).order_by('presenter')

print(len(moarefi_shode_ha))
# معرف ها
moaref_ha: list[Profile] = list[Profile]()
for a in moarefi_shode_ha:
    moaref: Profile = all_ashkhas.get(id=a.presenter.id)
    if not moaref in moaref_ha:
        moaref_ha.append(moaref)

print(len(moaref_ha))
for m in moaref_ha:
    print(f'{m} ;  {m.moarefi_shode_ha.all().count()} ; {m.mojodi_moarefishodeha_ta():,}')
