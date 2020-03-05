<H1>This project is for analyzing retail data and predicting sales and the chance of repurchasing</H1>

<p> Before Everything Else, for this project to work we need 
 PostgreSql Database Server which has to be started. 
 To make it work you have to insert your database configuration
 parameters in database.ini file. After Entering there you can edit
 schema_name`s, table names, types, column names and e.t.c in database.py.
  After everything I said above will be done, by running the project you will create
  schema, tables and relations in your database and the data will be stored.
  <b>To Run The project you need to run main.py</b></p>
  
Project Organization
------------

    ├── data
    │   ├── shortData      <- That is shorten version of original data for testing
    │   ├── raw            <- The original, immutable data dump.
    ├── database
    │   ├── config.py      <- This file is used to create database parameters for PostgreSql
    │   ├── database.ini   <- PostgreSql Configuration File 
    │   ├── database.py    <- Initializator for Database
    ├── main.py            <- main python file to run the project
    ├── README.md          <- The top-level README for developers using this project.
--------