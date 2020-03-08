from __future__ import division

import sys
from datetime import datetime, date

from pandas import DataFrame
from pandas.core.base import DataError
from sklearn import linear_model
import statsmodels.api as sm

# import libraries
from datetime import datetime, timedelta, date
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

# do not show warnings
import warnings

warnings.filterwarnings("ignore")

# import plotly for visualization
# import plotly.plotly as py
# import plotly.offline as pyoff
# import plotly.graph_objs as go

# import machine learning related libraries
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split

from database.database import Database, schema_name, invoice_table, invoice_product_table, product_table


def classification_model():
    try:
        database = Database()

        #
        query = f"""select it.invoice_date, it.customer_id, ipt.quantity, pt.price
                   from {schema_name}.{invoice_table} it
                        inner join {schema_name}.{invoice_product_table} ipt 
                            on it.invoice_no = ipt.invoice_no
                        inner join {schema_name}.{product_table} pt 
                            on ipt.stock_code = pt.stock_code
                    where it.customer_id <> 'NaN' and
					      left(it.invoice_no,1)<>'C'
                   order by it.invoice_date  """

        select = database.select(query)
        data = pd.DataFrame(select, columns=['InvoiceDate', 'Customer ID', 'Quantity', 'Price'])

        train_date_before = data[data['InvoiceDate'] < date(2011, 6, 1)].reset_index(drop=True)
        train_date_after = data[data['InvoiceDate'] >= date(2011, 6, 1)].reset_index(drop=True)

        customers = pd.DataFrame(train_date_before['Customer ID'].unique())
        customers.columns = ['Customer ID']

        # Create a Dataframe with Custoemr ID and First Purchase date after given Date
        customer_next_purchase = train_date_after.groupby('Customer ID').InvoiceDate.min().reset_index()
        customer_next_purchase.columns = ['Customer ID', 'MinPurchaseDate']

        # Create a Dataframe with Customer ID and last Purchase Date before given Date
        customer_last_purchase = train_date_before.groupby('Customer ID').InvoiceDate.max().reset_index()
        customer_last_purchase.columns = ['Customer ID', 'MaxPurchaseDate']

        # Merge two Dataframes
        purchase_dates = pd.merge(customer_last_purchase, customer_next_purchase, on='Customer ID', how='left')

        # Calculate the time difference in days
        purchase_dates['NextPurchaseDay'] = (
                purchase_dates['MinPurchaseDate'] - purchase_dates['MaxPurchaseDate']).dt.days

        # Merge with Customers
        customers = pd.merge(customers, purchase_dates[['Customer ID', 'NextPurchaseDay']], on='Customer ID',
                             how='left')

        # Fill NA values with 999
        customers = customers.fillna(999)

        # Recency

        # Max Purchase date for Recency
        max_purchase = train_date_before.groupby('Customer ID').InvoiceDate.max().reset_index()
        max_purchase.columns = ['Customer ID', 'MaxPurchaseDate']

        # Find the recency in days and add it to Customers
        max_purchase['Recency'] = (max_purchase['MaxPurchaseDate'].max() - max_purchase['MaxPurchaseDate']).dt.days
        customers = pd.merge(customers, max_purchase[['Customer ID', 'Recency']], on='Customer ID')

        """
        # Plot Recenct
        plot_data = [
            go.Histogram(
                x=customers['Recency']
            )
        ]

        plot_layout = go.Layout(
            title = 'Recency'
        )

        fig = go.Figure(data=plot_data, layout = plot_layout)

        pyoff.iplot(fig)

        """

        # Clustering for Recency
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(customers[['Recency']])
        customers['RecencyCluster'] = kmeans.predict(customers[['Recency']])

        # Order Recency Clusters
        customers = order_cluster('RecencyCluster', 'Recency', customers, False)

        # Print Cluster Characteristics
        customers.groupby('RecencyCluster')['Recency'].describe()

        # Get Total purchases for Frequency Scores
        frequency = train_date_before.groupby('Customer ID').InvoiceDate.count().reset_index()
        frequency.columns = ['Customer ID', 'Frequency']

        # Add Frequency column to Customers
        customers = pd.merge(customers, frequency, on='Customer ID')

        # Plot Frequency

        """
        plot_data = [
            go.Histogram(
                x=customers.query('Frequency < 1000')['Frequency']
            )
        ]

        plot_layout = go.Layout(
            title = 'Frequency'
        )

        fig = go.Figure(data=plot_data, layout = plot_layout)
        pyoff.iplot(fig)

        """
        # Clustering for Frequency

        kmeans = KMeans(n_clusters=4)
        kmeans.fit(customers[['Frequency']])
        customers['FrequencyCluster'] = kmeans.predict(customers[['Frequency']])

        # Order Frequency cluster and Show the Characteristics

        customers = order_cluster('FrequencyCluster', 'Frequency', customers, True)
        customers.groupby('FrequencyCluster')['Frequency'].describe()

        # Calculate monetary value, Create a Dataframe With it
        train_date_before['Revenue'] = train_date_before['Quantity'] * train_date_before['Price']
        train_date_before['Revenue'] = pd.to_numeric(train_date_before['Revenue'])
        revenue = train_date_before.groupby('Customer ID').Revenue.sum().reset_index()

        customers = pd.merge(customers, revenue, on='Customer ID')

        # Plot Revenue

        """
        plot_data = [
            go.Histogram (
                x = customers.query('Revenue < 1000')['Revenie']
            )
        ]

        plot_layout = go.Layout(
            title = 'Moonetary Value'
        )


        fig = go.Figure(data=plot_data, layout = plot_layout)
        pyoff.iplot(fig)
        """

        # Revenue Clusters
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(customers[['Revenue']])
        customers['RevenueCluster'] = kmeans.predict(customers[['Revenue']])

        # Ordering Clusters and who the Characteristics
        customers = order_cluster('RevenueCluster', 'Revenue', customers, True)
        customers.groupby('RevenueCluster')['Revenue'].describe()

        # Building overall Segmentation
        customers['OverallScore'] = customers['RecencyCluster'] + customers['FrequencyCluster'] \
                                    + customers['RevenueCluster']

        # Assign Segment Names
        customers['Segment'] = 'Low-Value'
        customers.loc[customers['OverallScore'] > 2, 'Segment'] = 'Mid-Value'
        customers.loc[customers['OverallScore'] > 4, 'Segment'] = 'High-Value'

        # Plot Revenue VS Frequency
        """
        graph = customers.query('Revenue < 5000 and Frequency < 2000')

        plot_data = [
            go.Scatter(
                x=graph.query("Segment == 'Low-Value'")['Frequency'],
                y=graph.query("Segment == 'Low-Value")['Revenue'],
                mode='markers',
                name='Low',
                marker=dict(size=7,
                            line=dict(width=1),
                            color='blue',
                            opacity=0.8)
            ),
            go.Scatter(
                x=graph.query("Segment == 'Mid-Value'")['Frequency'],
                y=graph.query("Segment == 'Mid-Value")['Revenue'],
                mode='markers',
                name='Mid',
                marker=dict(size=9,
                            line=dict(width=1),
                            color='green',
                            opacity=0.5)
            ),
            go.Scatter(
                x=graph.query("Segment == 'High-Value'")['Frequency'],
                y=graph.query("Segment == 'High-Value")['Revenue'],
                mode='markers',
                name='High',
                marker=dict(size=11,
                            line=dict(width=1),
                            color='red',
                            opacity=0.9)
            ),
        ]

        plot_layout = go.Layout(
            yaxis={'title': 'Revenue'},
            xaxis={'title': 'Frequency'},
            title='Segments'
        )

        fig = go.Figure(data=plot_data, layout=plot_layout)
        pyoff.iplot(fig)

        """

        # Create a Datafram with Custoemr ID and Invoice Date
        day_order = train_date_before[['Customer ID', 'InvoiceDate']]

        # Convert Invoice Datetime to day

        day_order['InvoiceDay'] = train_date_before['InvoiceDate']

        day_order = day_order.sort_values(['Customer ID', 'InvoiceDate'])

        # Drop Duplicates
        day_order = day_order.drop_duplicates(subset=['Customer ID', 'InvoiceDay'], keep='first')

        # Shifting last 3 Purchase dates
        day_order['PrevInvoiceDate'] = day_order.groupby('Customer ID')['InvoiceDay'].shift(1)
        day_order['T2InvoiceDate'] = day_order.groupby('Customer ID')['InvoiceDay'].shift(2)
        day_order['T3InvoiceDate'] = day_order.groupby('Customer ID')['InvoiceDay'].shift(3)

        day_order.head()

        # Find the Difference between days
        day_order['DayDiff'] = (day_order['InvoiceDay'] - day_order['PrevInvoiceDate']).dt.days
        day_order['DayDiff2'] = (day_order['InvoiceDay'] - day_order['T2InvoiceDate']).dt.days
        day_order['DayDiff3'] = (day_order['InvoiceDay'] - day_order['T3InvoiceDate']).dt.days

        # Find out the mean and standard devition of the diference between purchases in days

        day_diff = day_order.groupby('Customer ID').agg({'DayDiff': ['mean', 'std']}).reset_index()
        day_diff.columns = ['Customer ID', 'DayDiffMean', 'DayDiffStd']

        day_order_last = day_order.drop_duplicates(subset=['Customer ID'], keep='last')

        day_order_last = day_order_last.dropna()

        day_order_last = pd.merge(day_order_last, day_diff, on='Customer ID')

        customers = pd.merge(customers, day_order_last[
            ['Customer ID', 'DayDiff', 'DayDiff2', 'DayDiff3', 'DayDiffMean', 'DayDiffStd']], on='Customer ID')

        # Create the copy of Customer Dataframe to apply get_dummies

        customers_copy = customers.copy()
        customers_copy = pd.get_dummies(customers_copy)

        # customers.NextPurchaseDay.describe()
        abc = customers.NextPurchaseDay.describe()
        abc_fixed = abc.reset_index().replace(
            {'25%': '25_percent', '50%': '50_percent', '75%': '75_percent'}
        ).set_index('index')

        customers_copy['NextPurchaseDayRange'] = 2
        customers_copy.loc[customers_copy.NextPurchaseDay > 20, 'NextPurchaseDayRange'] = 1
        customers_copy.loc[customers_copy.NextPurchaseDay > 50, 'NextPurchaseDayRange'] = 0

        # corr = customers_copy[customers_copy.columns].corr()
        # plt.figure(figsize=(30,20))
        # sns.heatmap(corr, annot = True, linewidths=0.2, fmt=".2f")

        # Train and Test Split
        customers_copy = customers_copy.drop('NextPurchaseDay', axis=1)
        X, y = customers_copy.drop('NextPurchaseDayRange', axis=1), customers_copy.NextPurchaseDayRange

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

        # Create an array of models
        models = []
        models.append((('LR', LogisticRegression())))
        models.append(('NB', GaussianNB()))
        models.append(('RF', RandomForestClassifier()))
        models.append(('SVC', SVC()))
        models.append(("Dtree", DecisionTreeClassifier()))
        models.append(("KNN", KNeighborsClassifier()))

        # Measure the accuracy
        for name, model in models:
            kfold = KFold(n_splits=2, random_state=22)
            result = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
            print(name, result)

        model = LogisticRegression(solver='liblinear', random_state=0).fit(X_train, y_train)
        print('Debugger')

    except DataError as err:
        print('Data Error ', err)
    except TypeError as err:
        print('Type Error ', err)
    except KeyError as err:
        print('Key Error ', err)
    except SystemError as err:
        print('SystemError ', err)
    except AttributeError as err:
        print('Attribute Error ', err)
    except:
        print(sys.exc_info()[0])
        raise


# Order Cluster Method
def order_cluster(cluster_field_name, target_field_name, dataframe, ascending):
    new_cluster_field_name = 'new_' + cluster_field_name

    datafarme_new = dataframe.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    datafarme_new = datafarme_new.sort_values(by=target_field_name, ascending=ascending).reset_index(drop=True)
    datafarme_new['index'] = datafarme_new.index
    dataframe_final = pd.merge(dataframe, datafarme_new[[cluster_field_name, 'index']], on=cluster_field_name)
    dataframe_final = dataframe_final.drop([cluster_field_name], axis=1)
    dataframe_final = dataframe_final.rename(columns={'index': cluster_field_name})
    return dataframe_final
