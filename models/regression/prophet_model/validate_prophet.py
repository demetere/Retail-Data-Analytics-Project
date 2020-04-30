from math import sqrt
from sklearn.metrics import mean_squared_error


def validate_prophet(validation, predictions):

    mse = mean_squared_error(validation, predictions)
    rmse = sqrt(mse)
    print('RMSE: %.3f' % rmse)

    return rmse
