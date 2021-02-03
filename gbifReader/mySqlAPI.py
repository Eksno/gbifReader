import mysql.connector
from sqlalchemy import types, create_engine
import pandas as pd


class MySQLAPI:
    def __init__(self, host, user, password, database):
        print("\nInitialising API...")

        print(" - Connecting to database...")
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.host = host
        self.user = user
        self.password = password
        self.schema = database
        self.port = 3306

        self.engine = create_engine(f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.schema}',
                               echo=False)

        self.cursor = self.db.cursor()

        print(" / API initialised.")

    def clear(self, table):
        print(f"\nClearing {table}...")

        self.cursor.execute(f"TRUNCATE TABLE {table}")

        print(f" / {table} has been cleared.")

    def rowcount(self):
        return self.cursor.rowcount

    def df_to_db(self, table, data_df):
        data_df.to_sql(table, self.engine, if_exists='replace', chunksize=10000, dtype={"occurrenceID": types.VARCHAR(length=255)})

    def list_to_db(self, table, val):
        print(f"\nInserting list into {table}...")

        # Creates a string that contains column_names in a tuple like string.
        # Ex: (First Name, Last Name, Age)
        column_names = str(tuple(val[0])).replace('\'', '')

        # Creates a string that contains %s in a tuple like string
        # where the amount of %s is equal to the amount of columns.
        # Ex: (%s, %s, %s)
        column_value_template = str(tuple("%s" for _ in val[0])).replace('\'', '')

        # Creates an sql command able to insert a list of values into the table.
        sql = f"INSERT INTO {table} {column_names} VALUES {column_value_template}"

        # Inserts everything in the given list into the table
        self.cursor.executemany(sql, val[1:])

        self.db.commit()

        print(f" / {len(val) - 1} records inserted.")
        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return len(self.cursor.fetchall())

    def db_to_df(self, table, index_col=None):
        print(f"\nInserting {table} into dataframe...")
        result = pd.read_sql(f'SELECT * FROM {table}', con=self.engine, index_col=index_col)
        print(result)
        print(f" / Dataframe created.")
        return result

    def db_to_list(self, table):
        # Getting table as pandas dataframe
        df = self.db_to_df(table)

        # Converting dataframe to python list.
        return df.to_list()
