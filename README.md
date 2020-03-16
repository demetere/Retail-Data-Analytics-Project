<H1>This project is for analyzing retail data and predicting sales and the chance of repurchasing</H1>

<p> <b>To run this project you need to run main.py file and configure Database.
    Everything is written in those files and follow instructions to start
    the project</b></p>
  
Project Organization
------------

    ├── data
    │   ├── shortData                   <- That is shorten version of original data for testing
    │   ├── raw                         <- The original, immutable data dump.
    ├── database
    │   ├── config.py                   <- This file is used to create database parameters for PostgreSql
    │   ├── database.ini                <- PostgreSql Configuration File 
    │   ├── database.py                 <- Initializator for Database
    ├── models
    │   ├── regression
    │   │   ├──arima_model              <- arima model for regression task
    │   │   ├──prophet_model.py         <- prophet model for regression task
    │   ├── classification_model.py     <- model implementation for classification task
    │   ├── predict_model.py            <- prediction model, currently empty
    │   ├── regression_model.py         <- model implementation for regression task
    │   ├── train_model.py              <- train model, currently empty
    ├── main.py                         <- main python file to run the project
    ├── README.md                       <- The top-level README for developers using this project.
--------