import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNZ144.settings')
import django
django.setup()
from django.conf import settings


def main():
	from accounting import models as buh_model
	from accounts.models import ApiUser
	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/spreadsheets',
			'https://www.googleapis.com/auth/drive.file',
			'https://www.googleapis.com/auth/drive',
			]
	#TODO os.path()
	creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(settings.BASE_DIR, 'DNZ144-c13c1ab86ec0.json'), scope)
	client = gspread.authorize(creds)
	sheet = client.open('Names').worksheet('toys')
	# data = sheet.get_all_values()
	data = sheet.get_all_records()
	user = ApiUser.objects.first()
	for row in data:
		kassa = buh_model.Kassa.objects.get(name=row['Касса'])
		kassa.withdraw(row['Сумма'], user)
		# buh_model.Operation.objects.create(
		# 		kassa = buh_model.Kassa.objects.get(name=row['Касса']),
		# 		# kid = group_model.Kid.objects.get(id=row['№']),
		# 		# kid = group_model.Kid.objects.get(last_name=row['ФИО'].split()[0].strip()),
		# 		user = ApiUser.objects.first(),
		# 		trans_type = "CRE",
		# 		amount = row['Сумма'],
		# 		comment = row['Описание']
		# 	)
		print(row)



if __name__ == '__main__':
	main()
