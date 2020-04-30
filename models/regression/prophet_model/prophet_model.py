import pandas as pd
from database.database import Database
from fbprophet import Prophet

from models.regression.prophet_model.predict_prophet import predict_prophet
from models.regression.prophet_model.validate_prophet import validate_prophet


def prophet_model(config_file):
    database = Database(config_file)

    query = f"""select it.invoice_date date, sum(ipt.quantity) sale
                                   from retail_data.invoice it
                                        inner join retail_data.invoice_product ipt 
                                            on it.invoice_no = ipt.invoice_no
                                    where it.customer_id <> 'NaN' 
                                        and ipt.quantity>0
                					and left(it.invoice_no,1)<>'C'
                					group by (it.invoice_date)
                                    order by it.invoice_date   """

    select = database.select(query)
    sales = pd.DataFrame(select, columns=['Date', 'Sale'])
    sales['Date'] = pd.to_datetime(sales['Date'])

    sales = sales.rename(columns={'Date':'ds', 'Sale':'y'})

    # Split Data
    split_point = len(sales) - 14
    dataset, validation = sales[0:split_point], sales[split_point:]

    # Model
    model = Prophet()
    model.fit(dataset)

    # Predict
    forecast = predict_prophet(model, validation)

    validation_data = validation['y'].to_numpy().astype(float)
    prediction_data = forecast['Sale'].to_numpy()

    return validate_prophet(validation_data, prediction_data)

