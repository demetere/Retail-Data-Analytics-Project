import pandas as pd
import psycopg2
from sklearn import linear_model
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from database.database import Database


def main():

    # some practice with data

    data = pd.read_excel("data/shortData/online_retail_II.xlsx",
                         parse_dates=['InvoiceDate'],
                         converters={'StockCode': lambda x: str(x),
                                     'Invoice': lambda y: str(y)})

    register_matplotlib_converters()
    plt.scatter(data['Invoice'], data['Quantity'], color='red')
    plt.xlabel('Invoice', fontsize=14)
    plt.ylabel('Quantity', fontsize=14)
    plt.grid(True)
    plt.show()

    print("Debugger")


if __name__ == '__main__':


    database = Database()
    main()
