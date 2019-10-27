import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNZ144.settings')
import django
django.setup()
from django.conf import settings


def main():
	from group import models
	from accounting import models as buh
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

	# print(data)

	trans = buh.Operation
	kassa = buh.Kassa
	for entry in data:
		new_trans = trans.objects.create(
				kassa = kassa.objects.get(name=entry['fond']),
				kid =  models.Kid.objects.get(id=entry['kid_id']),
				trans_type = entry['trans_type'],
				amount = entry['amount'],
				comment = entry['comment'],
				user = ApiUser.objects.first()
			)
		new_trans.save()


	# for kid in data:
	# 	if len(kid["name"].split()) > 1:
	# 		kid_name = kid["name"].split()
	# 		new_kid = models.Kid.objects.create(last_name=kid_name[0], first_name=kid_name[1])
	# 	else:
	# 		new_kid = models.Kid.objects.create(last_name=kid["name"])
	# 	new_kid.save()

if __name__ == '__main__':
	main()
