"""
Module contain script for regular filling google sheet with operations data for each Kassa.
"""
import datetime
import os
#  GoogleAPI
import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials
#  Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNZ144.settings')
django.setup()
from django.conf import settings
#  ENV
import environ
#  Models
from accounting.models import Kassa

env = environ.Env()
environ.Env.read_env('dnz.env')


def main():
    """

    :return: string for success-mailing from the server.
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive',
             ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(settings.BASE_DIR, 'DNZ144-c13c1ab86ec0.json'), scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(env('SPREADSHEET')).worksheet(env("SHEET"))
    cursor = 2
    totals = []
    for kassa in Kassa.objects.filter(is_active=True):
        sheet.update_acell('A' + str(cursor), str(kassa))  
        cursor += 1   
        #  ONLY for 'Общий сбор'
        if kassa.name == 'Общий сбор':
            row = 1
            end_date = datetime.date(2020, 6, 1)
            start = datetime.date(2019, 10, 1)
            months = end_date
            step = 0
            months_list = []
            if end_date > start:
                while months >= start and step < 30:
                    step += 1
                    months_list.append("{}-{}".format(months.month, months.year))
                    if months.month <= 1:
                        months = months.replace(year=months.year - 1, month=12)
                        continue
                    months = months.replace(month=months.month - 1)
            months_list = months_list[::-1]
            cells_first_row = [Cell(cursor, i + 3, months_list[i]) for i in range(len(months_list))]
            sheet.update_cells(cells_first_row)
            cells_list = []
            for kid in kassa.group.kids.all():
                balance = float(kassa.kid_balance(kid)['deb'])
                withdraws = []
                for i in range(len(months_list)):
                    if i == 0:
                        if balance >= 50:
                            withdraws.append(50)
                            balance -= 50
                        elif balance > 0 and balance < 100:
                            withdraws.append(balance)
                            balance -= balance
                        elif balance == 0:
                            withdraws.append(0)
                    if balance >= 100:
                        withdraws.append(100)
                        balance -= 100
                    elif balance > 0 and balance < 100:
                        withdraws.append(balance)
                        balance -= balance
                    elif balance == 0:
                        withdraws.append(0)
                r_cell = row + cursor
                cells_list.append(Cell(r_cell, 1, int(row)))
                cells_list.append(Cell(r_cell, 2, kid.last_name))
                for i in range(len(months_list)):
                    cells_list.append(Cell(r_cell, i + 3, withdraws[i]))
                row += 1
            # rows = len(kassa.group.kids.all())
            kassa_total_cell = Cell(cursor + row, 5, float(kassa.get_saldo()))
            cells_list.append(kassa_total_cell)
            totals.append('E' + str(kassa_total_cell.row))
            sheet.update_cells(cells_list)
            cursor += row + 2
            continue
        row = 1
        r = str(cursor)
        sheet.update_acell('A' + r, '#')
        sheet.update_acell('B' + r, 'Фамилия')
        sheet.update_acell('C' + r, 'Поступление')
        sheet.update_acell('D' + r, 'Снятие')
        sheet.update_acell('E' + r, 'Баланс')
        cells_list = []
        for kid in kassa.group.kids.all():
            r = str(row + cursor)
            balance = kassa.kid_balance(kid)
            r_cell = row + cursor
            cells_list.append(Cell(r_cell, 1, int(row)))
            cells_list.append(Cell(r_cell, 2, kid.last_name))
            cells_list.append(Cell(r_cell, 3, float(balance['deb'])))
            cells_list.append(Cell(r_cell, 4, float(balance['cre'])))
            cells_list.append(Cell(r_cell, 5, float(balance['balance'])))
            row += 1
        sheet.update_cells(cells_list)
        sheet.update_acell('C' + str(int(r) + 1), f'=SUM(C{cursor}:C{str(r)})')
        sheet.update_acell('D' + str(int(r) + 1), f'=SUM(D{cursor}:D{str(r)})')
        kassa_total_cell = 'E' + str(int(r) + 1)
        sheet.update_acell(kassa_total_cell, f'=SUM(E{cursor}:E{str(r)})')
        totals.append(kassa_total_cell)
        cursor += 2
        cursor += row
    sheet.update_acell('G1', 'Последнее обновление:')
    sheet.update_acell('H1', str(datetime.datetime.now().replace(second=0, microsecond=0)))
    sheet.update_acell('G2', 'Общий баланс по фондам:')
    sheet.update_acell('H2', f"=SUM({','.join(totals)})")

    return "Таблица успешно обновлена: {time}".format(time=datetime.datetime.now().ctime())


if __name__ == '__main__':

    main()
