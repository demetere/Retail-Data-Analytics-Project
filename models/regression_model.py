from __future__ import division

import sys
from datetime import datetime, timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import warnings
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from keras.layers import LSTM
from sklearn.model_selection import KFold, cross_val_score, train_test_split

from database.database import Database

warnings.filterwarnings("ignore")


"""
#import Keras
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from keras.layers import LSTM
from sklearn.model_selection import KFold, cross_val_score, train_test_split
"""

from database.database import Database, schema_name, invoice_table, invoice_product_table, product_table


def regression_model():
    try:
        database = Database()

        #
        query = f"""select it.invoice_date date, sum(ipt.quantity) sale
                   from retail_data.invoice it
                        inner join retail_data.invoice_product ipt 
                            on it.invoice_no = ipt.invoice_no
                    where it.customer_id <> 'NaN' 
					and left(it.invoice_no,1)<>'C'
					group by (it.invoice_date)
                    order by it.invoice_date   """

        select = database.select(query)
        sales = pd.DataFrame(select, columns=['Date', 'Sale'])
        sales['Date'] = pd.to_datetime(sales['Date'])


        sales['Date'] = sales['Date'].dt.year.astype('str') + '-' + sales['Date'].dt.month.astype('str') + '-01'
        sales['Date'] = pd.to_datetime(sales['Date'])

        # Sum Up Daily Sales
        sales = sales.groupby('Date').Sale.sum().reset_index()

        #plt.plot(sales['Date'], sales['Sale'])
        #plt.show()

        # Make a copy of sales
        diff = sales.copy()

        # Add previous Sales to the next row
        diff['PrevSales'] = diff['Sale'].shift(1)

        # Drop the null values and calculate the difference
        diff = diff.dropna()
        diff['Diff'] = (diff['Sale'] - diff['PrevSales'])

        #plt.plot(diff['Date'], diff['Diff'])
        #plt.title('New One')
        #plt.show()

        # Create dataframe for transformation form time series to supervised
        supervised = diff.drop(['PrevSales'],axis=1)

        # Adding lags
        for inc in range (1,25):
            field_name = 'lag_' + str(inc)
            supervised[field_name] = supervised['Diff'].shift(inc)

        # Drop null values
        supervised = supervised.dropna().reset_index(drop=True)

        """
        # Import statsmoedls.formula.api
        import statsmodels.formula.api as smf

        # Define the regression formula
        model = smf.ols(formula='Diff ~ lag_1', data=supervised)

        # Fit the regression
        model_fit = model.fit()

        regression_adj_rsq = model_fit.rsquared_adj
        print(regression_adj_rsq)
        """

        # import MinMaxScaler and create a new dataframe for LSTM model
        from sklearn.preprocessing import MinMaxScaler
        model = supervised.drop(['Sales', 'Date'], axis=1)
        # split train and test set
        train_set, test_set = model[0:-6].values, model[-6:].values

        # Apply Min Max Scaler
        scaler = MinMaxScaler(feature_range=(-1,1))
        scaler = scaler.fit(train_set)

        # Reshape training set
        train_set = train_set.reshape(train_set.shpae[0], train_set.shape[1])
        train_set_scaled = scaler.transform(train_set)

        # Reshape test set
        test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
        test_set_scaled = scaler.transform(test_set)

        X_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1]
        X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])

        X_test, y_test = test_set_scaled[:, 1:], test_set_scaled[:, 0:1]
        X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])


        model = Sequential()
        model.add(LSTM(4, batch_input_shape=(1, X_train.shape[1],
                                             X_train.shpae[2]), stateful=True))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(X_train, y_train, nb_epoch=100, batch_size=1, verbose=1, shuffle=False)

        y_pred = model.predict(X_test, batch_size=1)

        print('Debugger')


    except:
        print(sys.exc_info()[0])
        raise
