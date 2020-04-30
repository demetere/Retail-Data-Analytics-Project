from math import sqrt
from keras.losses import mean_squared_error


def validate_arima(test, predictions):
    mse = mean_squared_error(test, predictions)
    rmse = sqrt(mse)
    print('RMSE: %.3f' % rmse)

    return rmse