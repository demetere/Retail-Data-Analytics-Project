import psycopg2

# Will be changed in Future
from database.config import config

"""
    --------------> for future connection to database

    connection = psycopg2.connect(user="username",
                                  password="password",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
                                  
select count(schema_name) check_existence
from information_schema.schemata
where schema_name = 'schema_name';

"""

schema_name = 'retail_demetre'  # Schema Name

# Table Names Which has to be created in Schema
invoice_table, product_table, invoice_product_table = 'invoice', 'product', 'invoice_product'

# Invoice Table Column Names
invoice_columns = [['invoice_no', 'varchar(7)'], ['invoice_date', 'date'],
                   ['customer_id', 'numeric(6)'], ['country', 'varchar(50)']]

# Product Table Column Names
product_columns = [['stock_code', 'varchar(10)'], ['description', 'varchar(100)'],
                   ['price', 'numeric(3,2)']]

# Invoice_Product Table Column Names
invoice_product_columns = [['stock_code', 'varchar(10)'], ['invoice_no', 'varchar(7)'],
                           ['quantity', 'numeric(3)']]

username, password, host, port, database = "postgres", "jr1kpoh2", "127.0.0.1", "5432", "postgres"


class Database:
    def __init__(self):
        # Class Constructor
        try:
            # params = config()

            # self.conn = psycopg2.connect(**params)  # Postgres Database
            self.conn = psycopg2.connect(user="postgres",
                                         password="jr1kpoh2",
                                         host="127.0.0.1",
                                         port="5432",
                                         database="postgres")
            self.curs = self.conn.cursor()  # Cursor Object for Database Operations
            self.initialize_database()


        except psycopg2.Error as err:
            print(f'Connection Error: {err}')

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

    def select(self, query):
        # Execute select in database
        return self.curs.execute(query).fetchall()

    def initialize_database(self):
        #initQuery = f"""
        #select count(schema_name) check_existence
        #from information_schema.schemata
        #where schema_name = '{schema_name}';
        #"""

        initQuery = 'select 2'
        checkSchema = self.curs.execute(initQuery)  # Execute Command

        print(checkSchema)

        # Create Schema and Tables
        query = f"""
        CREATE SCHEMA IF NOT EXISTS {schema_name};
        
        CREATE TABLE {schema_name}.{invoice_table} (
            {invoice_columns[0][0]} {invoice_columns[0][1]} PRIMARY KEY,
            {invoice_columns[1][0]} {invoice_columns[1][1]},
            {invoice_columns[2][0]} {invoice_columns[2][1]},
            {invoice_columns[3][0]} {invoice_columns[3][1]}
        );

        CREATE TABLE {schema_name}.{product_table} (
            {product_columns[0][0]} {product_columns[0][1]} PRIMARY KEY,
            {product_columns[1][0]} {product_columns[1][1]},
            {product_columns[2][0]} {product_columns[2][1]}
        );
        
        CREATE TABLE {schema_name}.{invoice_product_table} (
            {invoice_product_columns[0][0]}  {invoice_product_columns[0][1]} REFERENCES {schema_name}.{product_table} ({
        product_columns[0][0]}),
            {invoice_product_columns[1][0]}  {invoice_product_columns[1][1]} REFERENCES {schema_name}.{invoice_table} ({
        invoice_columns[0][0]}),
            {invoice_product_columns[2][0]}  {invoice_product_columns[2][1]} 
        );
        
        """
