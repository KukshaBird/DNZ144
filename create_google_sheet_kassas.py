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
    from gspread.models import Cell
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
        row = 1
        cells_list = []
        for kid in kassa.group.kids.all():
            r = str(row + cursor)
            balance = kassa.kid_balance(kid)
            cells_list.append(Cell(row + cursor, 1, float(row)))
            cells_list.append(Cell(row + cursor, 2, kid.last_name))
            cells_list.append(Cell(row + cursor, 3, float(balance['deb'])))
            cells_list.append(Cell(row + cursor, 4, float(balance['cre'])))
            cells_list.append(Cell(row + cursor, 5, float(balance['balance'])))
            row += 1
        sheet.update_cells(cells_list)
        sheet.update_acell('C' + str(int(r) + 1), f'=SUM(C{cursor}:E{str(r)})')
        sheet.update_acell('D' + str(int(r) + 1), f'=SUM(D{cursor}:E{str(r)})')
        sheet.update_acell('E' + str(int(r)+1), f'=SUM(E{cursor}:E{str(r)})')
        cursor += 1
        cursor += row
    sheet.update_acell('E' + str(cursor + 1), f'=SUM(E1:E{str(cursor - 1)})')

if __name__ == '__main__':
    main()
