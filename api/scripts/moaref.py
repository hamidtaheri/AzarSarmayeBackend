from django.db.models import QuerySet

from api.models import Profile

# همه
all_ashkhas:QuerySet[Profile] = Profile.objects.all()

# معرفی شده ها
moarefi_shode_ha: QuerySet[Profile] = all_ashkhas.filter(Moaref_Tbl_Ashkhas_id__isnull=False).order_by('Moaref_Tbl_Ashkhas_id_id')

# معرفی نشده ها
moarefi_na_shode_ha = all_ashkhas.filter(Moaref_Tbl_Ashkhas_id__isnull=True).order_by('Moaref_Tbl_Ashkhas_id_id')

print(len(moarefi_shode_ha))
# معرف ها
moaref_ha: list[Profile] = list[Profile]()
for a in moarefi_shode_ha:
    moaref: Profile = all_ashkhas.get(id=a.presenter.id)
    if not moaref in moaref_ha:
        moaref_ha.append(moaref)

print(len(moaref_ha))
for m in moaref_ha:
    print(m)
