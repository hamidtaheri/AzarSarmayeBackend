import api.models

m = api.models.Ashkhas.objects.get(id=2)
print(m)
ta = '2021-07-26'
seporde = m.tarakonesh_sum_ta(kind=1, ta=ta)
print(seporde)

bardasht_sod = m.tarakonesh_sum_ta(kind=3, ta=ta)
print(bardasht_sod)
