import psycopg2
import pandas as pd
from database.config import config

# Those are Structure for Database which can be changed. There are Table names, Column names, Schema names
# and e.t.c


schema_name = 'retail_data'  # Schema Name

# Table Names Which has to be created in Schema
invoice_table, product_table, invoice_product_table = 'invoice', 'product', 'invoice_product'

# Invoice Table Column Names
invoice_columns = [['invoice_no', 'varchar(7)'], ['invoice_date', 'date'],
                   ['customer_id', 'varchar(8)'], ['country', 'varchar(50)']]

# Product Table Column Names
product_columns = [['stock_code', 'varchar(20)'], ['description', 'varchar(250)'],
                   ['price', 'numeric(10,3)']]

# Invoice_Product Table Column Names
invoice_product_columns = [['invoice_no', 'varchar(7)'], ['stock_code', 'varchar(20)'],
                           ['quantity', 'numeric(8)']]

# File name from which data has to be read
file_name = "data/raw/online_retail_II.xlsx"


class Database:
    def __init__(self):
        # Class Constructor
        try:
            params = config()  # Get parameters for Connection

            self.conn = psycopg2.connect(**params)  # Postgres Database
            self.curs = self.conn.cursor()  # Cursor Object for Database Operations

            # Check if schema like that exists, if not then create and add data
            initQuery = f"""select count(schema_name) check_existence
                           from information_schema.schemata
                           where schema_name = '{schema_name}' """
            self.curs.execute(initQuery)  # Execute Command

            check = self.curs.fetchone()  # Get Data
            if check[0] == 0:
                self.initialize_database()


        except psycopg2.Error as err:
            print(f'Connection Error: {err}')

    def select(self, query):
        # Execute select in database
        return self.curs.execute(query).fetchall()

    def initialize_database(self):

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
            {invoice_product_columns[0][0]}  {invoice_product_columns[0][1]} REFERENCES {schema_name}.{invoice_table} 
        ({invoice_columns[0][0]}),
            {invoice_product_columns[1][0]}  {invoice_product_columns[1][1]} REFERENCES {schema_name}.{product_table} 
        ({product_columns[0][0]}),
            {invoice_product_columns[2][0]}  {invoice_product_columns[2][1]} 
        );

        """

        self.curs.execute(query)  # Execute Command
        self.conn.commit()  # Commit Changes

        self.add_data_from_file()  # Add Data in Database

    def add_data_from_file(self):
        data = pd.read_excel(file_name,
                             sheet_name = 'Year 2010-2011',
                             parse_dates=['InvoiceDate'],
                             converters={'StockCode': lambda x: str(x),
                                         'Invoice': lambda y: str(y),
                                         'Customer ID': lambda z: str(z)})
        maxDate = data['InvoiceDate'][len(data)-1]


        try:
            for i in range(len(data)-1, -1, -1):


                if abs(maxDate.date() - data['InvoiceDate'][i].date()).days <= 14:
                    # Check existence of Invoice, if it is new then insert into Database
                    check_invoice = f""" select count({invoice_columns[0][0]}) 
                                        from {schema_name}.{invoice_table} a
                                        where a.{invoice_columns[0][0]} = '{data['Invoice'][i]}'"""
                    self.curs.execute(check_invoice)  # Execute Command

                    if self.curs.fetchone()[0] == 0:
                        # Form Query
                        insert_invoice = f"""
                                        insert into {schema_name}.{invoice_table}
                                        values(%s,%s,%s,%s) """
                        self.curs.execute(insert_invoice, (data['Invoice'][i], data['InvoiceDate'][i],
                                                           data['Customer ID'][i], data['Country'][i]))  # Execute

                    # Check if product like that exists in Database
                    check_product = f"""
                            select count({product_columns[0][0]}) 
                            from {schema_name}.{product_table} a
                            where a.{product_columns[0][0]} = '{data['StockCode'][i]}'"""
                    self.curs.execute(check_product)

                    # If there is not Product like that Insert into Database
                    if self.curs.fetchone()[0] == 0:
                        insert_product = f"""
                                        insert into {schema_name}.{product_table}
                                        values(%s,%s,%s) """

                        self.curs.execute(insert_product, (data['StockCode'][i],
                                                           data['Description'][i], data['Price'][i]))  # Execute Command

                    # Query for insert into insert_invoice_product
                    insert_invoice_product = f"""
                                    insert into {schema_name}.{invoice_product_table}
                                    values('{data['Invoice'][i]}','{data['StockCode'][i]}',
                                    {data['Quantity'][i]}) """
                    self.curs.execute(insert_invoice_product)  # Execute Command
                    self.conn.commit()  # Commit Changes
                else:
                    break
            else:
                print('debugger')
        except psycopg2.Error as err:
            print(err)
