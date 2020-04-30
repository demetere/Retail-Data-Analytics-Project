from statsmodels.tsa.arima_model import ARIMA
import numpy

def finalize_arima_model(X):
    # Create a differenced series
    def difference(dataset, interval=1):
        diff = list()
        for i in range(interval, len(dataset)):
            value = dataset[i] - dataset[i - interval]
            diff.append(value)
        return numpy.array(diff)

    days_in_year = 365
    differenced = difference(X, days_in_year)

    # Fit Model
    model = ARIMA(differenced, order=(7, 0, 1))
    model_fit = model.fit(disp=0)
    return model_fit

