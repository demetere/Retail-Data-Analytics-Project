# Database Configuration
This directory is for the database configuration. I will explain every part of this
class. This class is created dynamically so you can change anything you like: Starting from 
schema name and ending with the column type. So First of all, lets declare some schema name, 
table names and its columns and types: 

``` bash
schema_name = 'retail_data'  # Schema Name

# Table Names Which has to be created in Schema
invoice_table, product_table, invoice_product_table = 'invoice', 'product', 'invoice_product'

# Invoice Table Column Names
invoice_columns = [['invoice_no', 'varchar(7)'], ['invoice_date', 'date'],
                   ['customer_id', 'varchar(8)'], ['country', 'varchar(50)']]

# Product Table Column Names
product_columns = [['stock_code', 'varchar(20)'], ['description', 'varchar(250)'],
                   ['price', 'numeric(10,2)']]

# Invoice_Product Table Column Names
invoice_product_columns = [['invoice_no', 'varchar(7)'], ['stock_code', 'varchar(20)'],
                           ['quantity', 'numeric(8)']]
```

As you can see everything we need to create database is declared there. 
Now we will also define the source file of the data, which would be imported to database lately.


``` bash
# File name from which data has to be read
file_name = "data/shortData/online_retail_II.xlsx"
```

Now lets define the class with consturctor: 

```bash
class Database:
    def __init__(self,config_path):
        # Class Constructor
        try:

            params = config(config_path)  # Get parameters for Connection

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
```

As you can see it is an simple functions and simple queries. We will talk about
configs a little later. If you wonder why I am checking the existence of the schema
I will answer you, because in ```self.initialize_database()``` in that part if 
database has not initialized yet we we are importing data to it. But if it is already 
created we are skipping step of importing.

This Class has few function and those are:
```select_query(self, query), initialize_database(self), add_data_from_file(self) ```

Now lets see how ```select_query(self, query)``` looks like: 

```bash
def select(self, query):
    # Execute select in database
    self.curs.execute(query)
    return self.curs.fetchall()
```
As I said it is simple function. Now lets see how ```initialize_database(self)``` looks like:
```bash
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
```

We are creating schema with all its tables and connections with the given names and order.

This function calls ```add_data_from_file()``` function and now we will see how it looks like: 
```bash
    def add_data_from_file(self):
        data = pd.read_excel(file_name,
                             parse_dates=['InvoiceDate'],
                             converters={'StockCode': lambda x: str(x),
                                         'Invoice': lambda y: str(y),
                                         'Customer ID': lambda z: str(z)})


        try:
            for i in range(len(data)-1, -1, -1):
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

        except psycopg2.Error as err:
            print(err)

```

As you can see we are reading the data from excel file , we are parsing dates, and converting 
**Stock Code**, **Invoice** and **Customer ID** into string because some of them have some letters
in them. After there we always check if that type of data is already created or not in database, if there
is not any data with this ID, we will insert int, It also goes with the products too. 

Now we will return to configuration. 
We have ```config.py``` file created in our project which reads database parameters, parse it and returns
to Database class to connect.

The implementation of the config is like this: 
```bash
def config(filename, section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgres
    db = {}

    # Checks to see if section (postgres) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    # Returns an error if a parameter is called that is not listed in the initialization file
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
```
I think everything is understandable there except database.ini file structure. Now I will show you 
the structure of it: 

```bash
[postgresql]
host=localhost
database=postgres
user=postgres
password=password
```

It has easiest structure you can imagine. So this is everything you can need to 
understand how this class works and you can freely change anything you want and it will
adapt to your changes. 
