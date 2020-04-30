from __future__ import division

import sys

from pandas.core.base import DataError

# import libraries
import pandas as pd

# do not show warnings
import warnings

from models.classification.predict import predict
from models.classification.prepare_data import prepare_data
from models.classification.select_best_model import select_best_model

warnings.filterwarnings("ignore")

# import machine learning related libraries
from sklearn.model_selection import train_test_split
from database.database import Database, schema_name, invoice_table, invoice_product_table, product_table


def classification_model(config_file):
    try:
        # Create Database object
        database = Database(config_file)

        # Prepare Query
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

        # Prepare_data
        customers_copy = prepare_data(data)

        # Train and Test Split
        customers_copy = customers_copy.drop('NextPurchaseDay', axis=1)
        X, y = customers_copy.drop('NextPurchaseDayRange', axis=1), customers_copy.NextPurchaseDayRange

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

        # Select Best Model
        model = select_best_model(X_train, y_train, X_test, y_test)

        # Predict
        customers = predict(model, customers_copy)

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
