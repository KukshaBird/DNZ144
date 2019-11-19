import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNZ144.settings')
import django

django.setup()
from django.conf import settings


def main():
    from group.models import Group, Kid
    from accounting.models import Kassa
    from accounts.models import ApiUser
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive',
             ]
    # TODO os.path()
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(settings.BASE_DIR, 'DNZ144-c13c1ab86ec0.json'), scope
    )
    client = gspread.authorize(creds)
    sheet = client.open('Names').worksheet('tests')

    kids_num = Group.objects.first().kids.all().count()
    cursor = 1

    for kassa in Kassa.objects.all():
        sheet.update_acell('A' + str(cursor), str(kassa))
        cursor += 1
        r = str(cursor)
        sheet.update_acell('A' + r, '#')
        sheet.update_acell('B' + r, 'Фамилия')
        sheet.update_acell('C' + r, 'Поступление')
        sheet.update_acell('D' + r, 'Снятие')
        sheet.update_acell('E' + r, 'Баланс')
        # cursor += 1
        row = 1
        for kid in kassa.group.kids.all():
            r = str(row + cursor)
            balance = kassa.kid_balance(kid)
            sheet.update_acell('A' + r, str(row))
            sheet.update_acell('B' + r, kid.last_name)
            sheet.update_acell('C' + r, str(balance['deb']))
            sheet.update_acell('D' + r, str(balance['cre']))
            sheet.update_acell('E' + r, str(balance['balance']))
            row += 1
        cursor += row
        time.sleep(100)

if __name__ == '__main__':
    main()
