import time
import csvAPI
import requests
import pandas as pd
import request_download

from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
from mySqlAPI import MySQLAPI
from zipfile import BadZipFile


def main():
    if 'y' == input("Do you want to update the csv? (y, N)\n"):
        #DOWNLOAD_ID = request_download.send_request()

        #print(DOWNLOAD_ID)

        #bad_zip_file = True

        #progress = 0
        #while bad_zip_file:
            #try:

        DOWNLOAD_ID = '0127923-200613084148143'

        r = requests.get(f"https://api.gbif.org/v1/occurrence/download/request/{DOWNLOAD_ID}.zip")

        zipfile = ZipFile(BytesIO(r.content))

        filenames = zipfile.namelist()

        val = zipfile.open(filenames[0]).read()

        # Splitter opp tabs og linjeskift
        data_list = [x.split('\\t') for x in str(val).split('\\n')]

        excluded_columns = ["mediaType", "issue"]

        # Sender dict til apiet som konverterer den til en csv fil
        csvAPI.list_to_csv('csv/data.csv', data_list[:1002], excluded_columns)

    if 'y' == input("\nDo you want to update the table 'gbif_occurences'? (y, N)\n"):
        host, user, password, database, table = get_login_details()

        my_sql_api = MySQLAPI(host, user, password, database)

        # Upload csv to database table 'gbif_occurrences'
        data_df = csvAPI.csv_to_df('csv/data.csv', index_col='occurrenceID')

        data_df["lastInterpreted"] = pd.to_datetime(datetime.now())

        my_sql_api.df_to_db('gbif_occurrences', data_df)

    if 'y' == input("\nDo you want to update the table 'taxon'? (y, N)\n"):
        pass
        # Create table 'taxon' that contains taxon.
        host, user, password, database, table = get_login_details()

        my_sql_api = MySQLAPI(host, user, password, database)

        occurrences = my_sql_api.db_to_df('gbif_occurrences')

        taxon = occurrences[['key', 'nubKey', 'nameKey', 'taxonID', 'sourceTaxonKey', 'kingdom', 'phylum', 'order',
                             'family', 'kingdomKey', 'phylumKey', 'classKey', 'orderKey', 'familyKey', 'datasetkey',
                             'constituentKey', 'parentKey', 'parent', 'scientificName', 'canonicalName', 'authorship',
                             'nameType', 'rank', 'origin', 'taxonomicStatus', 'remarks', 'numDescendants',
                             'lastCrawled', 'lastInterpreted', 'synonym', 'class']].copy()

        my_sql_api.df_to_db('taxon', taxon)


def get_login_details():
    try:
        login_details = csvAPI.csv_to_dict('csv/databases.csv')
        host = login_details["host"][0]
        user = login_details["user"][0]
        password = login_details["password"][0]
        database = login_details["database"][0]
        table = login_details["table"][0]

    except FileNotFoundError:
        host = input("host: ")
        user = input("user: ")
        password = input("password: ")
        database = input("database: ")
        table = input("table: ")

    return host, user, password, database, table


if __name__ == '__main__':
    main()
