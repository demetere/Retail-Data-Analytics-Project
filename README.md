<H1>This project is for analyzing retail data for predicting sales and the chance of repurchasing</H1>

<H5>About This Project: I have researched many models to predict customers behaviour
  and sales. I may say that I can predict customers behaviour very well, with 
  approximately 95% percent accuracy with given data. That model was successful 
  and recommend to use it.  
  I also researched many models for future sales, but I could not find the best 
  solution yet, Despite that I have presented 3 models that you can look at. 
  As I said before, they are not the best ones, but they are still working 
  with low accuracy compared to the model I mentioned above. I am still researching
  some solutions and models to solve "Future Sales" problem. 
  </H5>






<p> <b>Insturctions: </b>To run this project you need to run main.py file and configure Database.
    Everything is written in those files and follow instructions to start
    the project</p> 
  
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