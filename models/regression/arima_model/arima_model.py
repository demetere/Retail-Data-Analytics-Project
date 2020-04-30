import pandas as pd
from database.database import Database

from models.regression.arima_model.finalize_arima_model import finalize_arima_model
from models.regression.arima_model.predict_arima import predict_arima
from models.regression.arima_model.validate_arima import validate_arima


def arima_model(config_file):

    database = Database(config_file)
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
    sales.set_index(['Date'], inplace=True)

    split_point = len(sales) - 14
    dataset, validation = sales[0:split_point], sales[split_point:]
    X = dataset.values

    model = finalize_arima_model(X)
    prediction = predict_arima(model, X)

    validation_data = validation['Sale'].to_numpy().astype(float)
    prediction_data = prediction.astype(float)
    return validate_arima(validation_data, prediction_data)
