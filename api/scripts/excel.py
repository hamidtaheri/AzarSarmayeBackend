from api.views import excel_to_bank_export_paya

path = "/Users/alamalhoda/Projects/AzarSaryame/backend/api/scripts/"
in_file = f'{path}{"paya-new_3.xlsx"}'
out_file = f'{path}{"paya-new_6.ccti"}'
# ExcelReader.paya_export(in_file=in_file, out_file=out_file, sum=132072511850, count=847)
excel_to_bank_export_paya(in_file=in_file, out_file=out_file, sum=13207251185, count=847)
