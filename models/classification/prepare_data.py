from __future__ import division

# import libraries
from datetime import date
import pandas as pd

# do not show warnings
import warnings

from models.classification.feature_engineering import feature_engineering

warnings.filterwarnings("ignore")


def prepare_data(data):
    train_date_before = data[data['InvoiceDate'] < date(2011, 11, 25)].reset_index(drop=True)
    train_date_after = data[data['InvoiceDate'] >= date(2011, 11, 25)].reset_index(drop=True)

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

    return feature_engineering(train_date_before, customers)

