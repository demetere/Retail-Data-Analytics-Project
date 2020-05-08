# Machine Learning

## Introduction
In this project we will use some machine learning algorithms and models to 
predict retail sales. We will be using many models. We will test them and will check
their score which represent how good is that model on that data. 

## Project intro/Objective
The purpose of this project is to predict some values with the given data. In particular, we have
predict the number of sales of last 14 days and the customer which will repurchase within last 14 days.
So to sum up it breaks down to two goals, those are:
* We have to predict whether customer will repurchase or not within 
last 14 days for given data
* We have to predict daily sales for the last 14 days.

So the two goals divide our project into two parts. One is the part of the solving **Classification** problem
which will be the first goal and the second will be solving the **Regression** problem.

## Project Description
As you already know our main goals are to predict values of different kind.
One will refer to ***Classification*** task and the other one will refer to ***Regression*** task.
We are using the methods which represents each kind of task. We will be using some very well known methods and for 
Classification task we will make  some feature engineering which will improve the accuracy of the model. 
For regression task we will not be using feature engineering and you will see that those models will not be 
so good without features. The dataset and the methods are described below.

## Dataset
We have the online data which can be downloaded with the format of **csv** or **xlsx** and
you can import it in your project. But we are using different approach. We are importing this data
into **Postgres** Database and we are collecting the data from there. The link to the data is like this: 

https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

Now lets describe the dataset:
* **InvoiceNo:** Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation. 
* **StockCode:** Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product. 
* **Description:** Product (item) name. Nominal. 
* **Quantity:** The quantities of each product (item) per transaction. Numeric.	
* **InvoiceDate:** Invice date and time. Numeric. The day and time when a transaction was generated. 
* **UnitPrice:** Unit price. Numeric. Product price per unit in sterling (Â£). 
* **CustomerID:** Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer. 
* **Country:** Country name. Nominal. The name of the country where a customer resides.

## Used Methods and Technologies
#### Methods Used
+ Machine Learning
+ Data Visualization
+ Predictive Modeling
+ etc.

#### Technologies

+ Python
+ PostGres
+ Pandas, jupyter
+ etc.

#### Machine Learning Methods Used
##### Regressions Task:
+ ARIMA
+ Prophet
##### Classification Task:
+ LogisticRegression
+ GaussianNB
+ RandomForestClassifier
+ SVC
+ DecisionTreeClassifier
+ XGBClassifier
+ KNeighborsClassifier
  

## How to run project
First of all, you need ro request a pull, after that u will be needed to install some dependencies
with the next command:
```bash
& pip install -r requirements.txt
```

After that it would be good if you looked at database schemas and configuration which is in database
folder and make fit with your database. Lastly, you can run `main.py` file,
you can change parameters all you want and test those models.


## Result/Report
You can find our results in the corresponding jupyter notebooks. We have 4 notebook. We have two for ***Regressoin***
task: 
+ [Arima Model Juptyer Notebook](models/regression/arima_model/arima_model_jupy.ipynb)
+ [Prophet Model Juptyer Notebook](models/regression/prophet_model/prophet_model_jupy.ipynb)

One notebook for comparing those two models: 
+ [Juptyer Notebook for Comparing Two Regressiong Model](models/regression/compare_models_jupy.ipynb)

And the one for ***Classification Task***:
+ [Classification Jupyter Notebook](models/classification/classification.ipynb)

## Project Organization
Now in this part we will review the project structure and how organized it is. So 
we have two task which will be solved by classification algorithms and regression algorithms and in
addition to this we are using database for data storing. So we have Three main folder and those are:
* data
* database
* models

In data there is dataset downloaded from the link above. In the database folder we have
database class implementation and database configuration. finally we have models folder.
Because of the given tasks it is dived by two. 
* regression
* classification

We are solving regression task with the two models. and those are **ARIMA** model and 
**Prophet** model, so we have that two folder in regression directory. In each directory we
have **Jupyter Notebook** representing the whole process of the handling those tasks. 
In regression folder we have one additional Jupyter Notebook which compares the presented regression
models and making conclusion about it.

In classification folder we also have **Jupyter Notebook** which refers the problem solving 
of classification task. 

Now here it is the organization of project.

------------

    ├── data
    │   ├── shortData                           <- That is shorten version of original data for testing
    │   ├── raw                                 <- The original, immutable data dump.
    ├── database
    │   ├── config.py                           <- This file is used to create database parameters for PostgreSql
    │   ├── database.ini                        <- PostgreSql Configuration File 
    │   ├── database.py                         <- PostgreSql Configuration File 
    │   ├── README.md                           <- The top-level readme for the class structure and purpose
    ├── models
    │   ├── regression
    │   │   ├── arima_model                  
    │   │   │   ├── arima_model.py              <- main class of solving the regressoing task with arima
    │   │   │   ├── arima_model_jupy.ipynb      <- Jupyter Notebook of the arima model.   
    │   │   │   ├── finalize_arima_model.py     <- creating the model of ARIMA     
    │   │   │   ├── predict_arima.py            <- making predictions with the trained model of ARIMA
    │   │   │   ├── validate_arima.py           <- valdiating model with testing out the score of it
    │   │   ├── prophet_model               
    │   │   │   ├── predict_prophet.py          <- making predictions with the trained model of Prophet
    │   │   │   ├── prophet_model.py            <- main class of solving the regressoing task with prophet
    │   │   │   ├── prophet_model_jupy.ipynb    <- Jupyter Notebook of the prophet model.      
    │   │   │   ├── validate_prophet.py         <- valdiating model with testing out the score of it  
    │   │   ├── compare_models_jupy.ipynb       <- comparing arima and prophet models
    │   ├── classification      
    │   │   ├── classification.ipynb            <- Jupyter Notebook for the classification model.     
    │   │   ├── classification_model.py         <- main class of solving the classification task 
    │   │   ├── feature_engineering.py          <- creating features for the model 
    │   │   ├── predict.py                      <- making predictions with the trained model
    │   │   ├── prepare_data.py                 <- main class of preparing data for the training and prediction
    │   │   ├── select_best_model.py            <- class for the selection of the best model for the given data
    ├── main.py                                 <- main python file to run the project
    ├── README.md                               <- The top-level README for developers using this project.
    ├── requirements.txt                        <- the libraries which will be needed for the project
--------




