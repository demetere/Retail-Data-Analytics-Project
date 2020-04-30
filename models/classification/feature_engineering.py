from __future__ import division

# import libraries
import pandas as pd
from sklearn.cluster import KMeans

# do not show warnings
import warnings

warnings.filterwarnings("ignore")


def feature_engineering(train_date_before, customers):
    # Recency

    # Max Purchase date for Recency
    max_purchase = train_date_before.groupby('Customer ID').InvoiceDate.max().reset_index()
    max_purchase.columns = ['Customer ID', 'MaxPurchaseDate']

    # Find the recency in days and add it to Customers
    max_purchase['Recency'] = (max_purchase['MaxPurchaseDate'].max() - max_purchase['MaxPurchaseDate']).dt.days
    customers = pd.merge(customers, max_purchase[['Customer ID', 'Recency']], on='Customer ID')

    # Clustering for Recency
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(customers[['Recency']])
    customers['RecencyCluster'] = kmeans.predict(customers[['Recency']])

    # Order Cluster Method
    def order_cluster(cluster_field_name, target_field_name, dataframe, ascending):
        datafarme_new = dataframe.groupby(cluster_field_name)[target_field_name].mean().reset_index()
        datafarme_new = datafarme_new.sort_values(by=target_field_name, ascending=ascending).reset_index(drop=True)
        datafarme_new['index'] = datafarme_new.index
        dataframe_final = pd.merge(dataframe, datafarme_new[[cluster_field_name, 'index']], on=cluster_field_name)
        dataframe_final = dataframe_final.drop([cluster_field_name], axis=1)
        dataframe_final = dataframe_final.rename(columns={'index': cluster_field_name})
        return dataframe_final

    # Order Recency Clusters
    customers = order_cluster('RecencyCluster', 'Recency', customers, False)

    # Get Total purchases for Frequency Scores
    frequency = train_date_before.groupby('Customer ID').InvoiceDate.count().reset_index()
    frequency.columns = ['Customer ID', 'Frequency']

    # Add Frequency column to Customers
    customers = pd.merge(customers, frequency, on='Customer ID')

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

    customers_copy['NextPurchaseDayRange'] = 1
    customers_copy.loc[customers_copy.NextPurchaseDay > 14, 'NextPurchaseDayRange'] = 0

    return customers_copy