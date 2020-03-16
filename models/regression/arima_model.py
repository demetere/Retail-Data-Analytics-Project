from decimal import Decimal
import numpy
import pandas as pd
from database.database import Database
from statsmodels.tsa.arima_model import ARIMA


def arima_model():
    def difference(dataset, interval=1):
        diff = list()
        for i in range(interval, len(dataset)):
            value = dataset[i] - dataset[i - interval]
            diff.append(value)
        return numpy.array(diff)

    # invert differenced value
    def inverse_difference(history, yhat, interval=1):
        return float(Decimal(yhat) + history[-interval])



    database = Database()
    query = f"""select it.invoice_date date, sum(ipt.quantity) sale
                       from retail_data.invoice it
                            inner join retail_data.invoice_product ipt 
                                on it.invoice_no = ipt.invoice_no
                        where it.customer_id <> 'NaN' 
    						--and ipt.stock_code = '21931'
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
    days_in_year = 365
    differenced = difference(X, days_in_year)

    # Fit Model
    model = ARIMA(differenced, order=(7, 0, 1))
    model_fit = model.fit(disp=0)

    start_index = len(differenced)
    end_index = start_index + 13
    forecast = model_fit.forecast(steps=14)[0]

    history = [x for x in X]
    day = 1

    for yhat in forecast:
        inverted = inverse_difference(history, yhat, days_in_year)
        print('Day %d: %f' % (day, inverted))
        history.append(inverted)
        day += 1

    print('Debugger')

