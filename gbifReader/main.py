import request_download
import requests
from zipfile import ZipFile
from io import BytesIO
from csvReader import csv_to_list
from mySqlAPI import MySQLAPI


def main():
    if 'y' == input("Do you want to update the csv? (y, n)\n"):
        DOWNLOAD_ID = request_download.send_request()

        r = requests.get("https://api.gbif.org/v1/occurrence/download/request/{}.zip".format(DOWNLOAD_ID))

        zipfile = ZipFile(BytesIO(r.content))

        filenames = zipfile.namelist()

        csv = zipfile.open(filenames[0]).read()

        with open('data.csv', 'wb') as f:
            f.write(csv)

    if 'y' == input("\nDo you want to update the database? (y, n)\n"):
        val = csv_to_list('data.csv')

        host, user, password, database, table = get_login_details()

        my_sql_api = MySQLAPI(host, user, password, database)

        my_sql_api.clear(table)

        my_sql_api.list_to_db(table, val)


def get_login_details():
    try:
        login_details = csv_to_list('databases.csv')[1]
        host = login_details[0]
        user = login_details[1]
        password = login_details[2]
        database = login_details[3]
        table = login_details[4]
    except FileNotFoundError:
        host = input("host: ")
        user = input("user: ")
        password = input("password: ")
        database = input("database: ")
        table = input("table: ")
    return host, user, password, database, table


if __name__ == '__main__':
    main()
