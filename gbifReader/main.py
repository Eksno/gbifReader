import sys
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
    host, user, password, database, table = get_login_details()

    my_sql_api = MySQLAPI(host, user, password, database)

    occurrences = my_sql_api.db_to_df('gbif_occurrences', index_col='occurrenceID')

    csvAPI.df_to_csv('csv/fake_database.csv', occurrences)

    if 'y' == input("\nDo you want to clear the table `gbif_occurrences`? (y, N)\n"):
        my_sql_api.clear('gbif_occurrences')

    if 'y' == input("\nDo you want to update the csv? (y, N)\n"):
        try:
            occurrences = my_sql_api.db_to_df('gbif_occurrences', index_col='occurrenceID')

            # Get the first date and month along with the newest date from `updated` in the format `yyyy-mm-dd`.
            first_year = str(min(occurrences["year"]))
            first_month = str(min(occurrences["month"]))
            last_update = str(max(pd.to_datetime(occurrences['updated'], format="%Y-%m-%d").dt.date))

            DOWNLOAD_ID = request_download.send_request(first_year, first_month, last_update)

        except:
            print("Failed to get reference data, ignoring previous data...")
            #DOWNLOAD_ID = request_download.send_request()
            #DOWNLOAD_ID = '0181694-200613084148143'

        print("\nDowloading data...")
        bad_zip_file = True
        progress = 0
        while bad_zip_file:
            try:
                r = requests.get(f"https://api.gbif.org/v1/occurrence/download/request/{DOWNLOAD_ID}.zip")

                zipfile = ZipFile(BytesIO(r.content))

                filenames = zipfile.namelist()

                val = zipfile.open(filenames[0]).read()

                # Splitter opp tabs og linjeskift
                data_list = [x.split('\\t') for x in str(val).split('\\n')]

                excluded_columns = ["mediaType", "issue"]

                # Sender dict til apiet som konverterer den til en csv fil
                csvAPI.list_to_csv('csv/data.csv', data_list, excluded_columns)
                bad_zip_file = False
                print(" / Finished.")
            except BadZipFile:
                sys.stdout.write(f'\r - Elapsed time: {progress} seconds.')
                time.sleep(0.1)
                progress += 1
                time.sleep(0.9)

    if 'y' == input("\nDo you want to update the table 'gbif_occurences'? (y, N)\n"):
        # Upload csv to database table 'gbif_occurrences'
        data_df = csvAPI.csv_to_df('csv/data.csv', index_col='occurrenceID')

        data_df["updated"] = pd.to_datetime(datetime.now())

        occurrences = my_sql_api.db_to_df('gbif_occurrences', index_col='occurrenceID')
        output = data_df.combine_first(occurrences)

        my_sql_api.df_to_db('gbif_occurrences', output)

    if 'y' == input("\nDo you want to update the table 'taxon'? (y, N)\n"):
        pass
        # Create table 'taxon' that contains taxon.
        occurrences = my_sql_api.db_to_df('gbif_occurrences', index_col='occurrenceID')

        taxon = occurrences[['key', 'nubKey', 'nameKey', 'taxonID', 'sourceTaxonKey', 'kingdom', 'phylum', 'order',
                             'family', 'kingdomKey', 'phylumKey', 'classKey', 'orderKey', 'familyKey', 'datasetkey',
                             'constituentKey', 'parentKey', 'parent', 'scientificName', 'canonicalName', 'authorship',
                             'nameType', 'rank', 'origin', 'taxonomicStatus', 'remarks', 'numDescendants',
                             'lastCrawled', 'lastInterpreted', 'synonym', 'class']].copy()

        my_sql_api.df_to_db('taxon', taxon)

    occurrences = my_sql_api.db_to_df('gbif_occurrences', index_col='occurrenceID')

    csvAPI.df_to_csv('csv/fake_database.csv', occurrences)


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
