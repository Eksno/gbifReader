import mysql.connector


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

        self.cursor = self.db.cursor()

        print(" / API initialised.")

    def clear(self, table):
        print(f"\nClearing {table}...")

        self.cursor.execute(f"TRUNCATE TABLE {table}")

        print(f" / {table} has been cleared.")

    def rowcount(self, table):
        return self.cursor.rowcount

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

    def db_to_list(self, table):
        print(f"\nInserting {table} into list...")

        self.cursor.execute(f"SELECT * FROM {table}")

        rows = [row for row in self.cursor.fetchall()]

        print(f" / {len(rows)} records collected.")
        return rows
