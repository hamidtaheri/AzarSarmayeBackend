from api.views import excel_to_bank_export_paya

path = "/Users/alamalhoda/Projects/AzarSaryame/backend/api/scripts/"
in_file = f'{path}{"paya-new.xlsx"}'
out_file = f'{path}{"paya-new_2.ccti"}'
# ExcelReader.paya_export(in_file=in_file, out_file=out_file, sum=132072511850, count=847)
excel_to_bank_export_paya(in_file=in_file, out_file=out_file, sum=132072511850, count=847)
