import pandas as pd
from database.database import Database
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet

database = Database()
def prophet_func():
    query = f"""select it.invoice_date date, sum(ipt.quantity) sale
                                   from retail_data.invoice it
                                        inner join retail_data.invoice_product ipt 
                                            on it.invoice_no = ipt.invoice_no
                                    where it.customer_id <> 'NaN' 
                                        and ipt.quantity>0
                						--and ipt.stock_code = '21931'
                					and left(it.invoice_no,1)<>'C'
                					group by (it.invoice_date)
                                    order by it.invoice_date   """

    select = database.select(query)
    sales = pd.DataFrame(select, columns=['Date', 'Sale'])
    sales['Date'] = pd.to_datetime(sales['Date'])
    #sales.set_index(['Date'], inplace=True)

    sales = sales.rename(columns={'Date':'ds', 'Sale':'y'})

    model = Prophet()
    model.fit(sales)

    range = pd.date_range('2011-12-09', periods=14, freq='D')

    future_dataframe = pd.DataFrame({'ds': range})


    forecast = model.predict(future_dataframe)

    forecast = forecast[['ds', 'yhat']]

    forecast = forecast.rename(columns={'ds':'Date', 'yhat':'Sale'})

    print(forecast)

