from django.db.models import QuerySet

from api.models import Ashkhas

# همه
all_ashkhas:QuerySet[Ashkhas] = Ashkhas.objects.all()

# معرفی شده ها
moarefi_shode_ha: QuerySet[Ashkhas] = all_ashkhas.filter(Moaref_Tbl_Ashkhas_id__isnull=False).order_by('Moaref_Tbl_Ashkhas_id_id')

# معرفی نشده ها
moarefi_na_shode_ha = all_ashkhas.filter(Moaref_Tbl_Ashkhas_id__isnull=True).order_by('Moaref_Tbl_Ashkhas_id_id')

print(len(moarefi_shode_ha))
# معرف ها
moaref_ha: list[Ashkhas] = list[Ashkhas]()
for a in moarefi_shode_ha:
    moaref: Ashkhas = all_ashkhas.get(id=a.Moaref_Tbl_Ashkhas_id.id)
    if not moaref in moaref_ha:
        moaref_ha.append(moaref)

print(len(moaref_ha))
for m in moaref_ha:
    print(m)
