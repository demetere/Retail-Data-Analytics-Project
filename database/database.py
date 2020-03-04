import psycopg2

### Will be changed in Future
"""""
    --------------> for future connection to database

    connection = psycopg2.connect(user="username",
                                  password="password",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

"""""


class Database:
    def __init__(self, base, table_name, table_columns):
        # Class Constructor
        try:
            self.conn = psycopg2.connect(base)  # Postgres Database
            self.curs = self.conn.cursor()  # Cursor Object for Database Operations
            self.table_name = table_name  # Table Name
            self.table_columns = [el[0] for el in table_columns]  # Columns
            self.create_table(table_columns)  # Create Table
        except psycopg2.Error as err:
            print(f'Connection Error: {err}')

    def drop_table(self):
        # Drop Table
        comm = f""" drop table if exists {self.table_name} """
        self.curs.execute(comm)  # Execute Command
        self.conn.commit()  # Commit Changes

    def create_table(self, table):
        # Create Table

        # Statement of Creation of Table
        comm = f""" create table if not exists {self.table_name} (Id integer primary key,\n"""
        for i in range(len(table)):
            comm += f"        {table[i][0]} {table[i][1]},\n"
        else:
            comm = comm[:-2] + "  )"
        self.curs.execute(comm)  # Execute Statement
        self.conn.commit()  # Commit Changes

    def add_record(self, crash):

        # Form the Statement
        comm = f""" insert into {self.table_name}("""
        for col in self.table_columns:
            comm += f"{col}, "
        else:
            comm = comm[:-2] + ")\n values ( "
        comm = comm[:-1] + crash.year + ', '
        comm = comm[:-1] + '"' + crash.accident + '", '
        comm = comm[:-1] + '"' + crash.time + '", '
        comm = comm[:-1] + '"' + crash.weather + '", '
        comm = comm[:-1] + '"' + crash.surface + '")'

        self.curs.execute(comm)  # Execute Command
        self.conn.commit()  # Commit Changes

    def update_record(self, ident, column, new_value):
        # Update record by ID
        comm = f""" update {self.table_name} set {column} = {new_value} where Id = {ident} """
        self.curs.execute(comm)  # Execute Command
        self.conn.commit()  # Commit Changes

    def get_one_record(self, ident):
        # Get One Record by ID
        comm = f""" select * from {self.table_name} where Id = {ident} """
        return self.curs.execute(comm).fetchall()[0]  # Execute Command

    def select(self, query):
        # Execute select in database
        return self.curs.execute(query).fetchall()
