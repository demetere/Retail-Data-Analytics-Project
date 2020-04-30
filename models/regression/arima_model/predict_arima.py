from decimal import Decimal



def predict_arima(model_fit, X):

    # invert differenced value
    def inverse_difference(history, yhat, interval=1):
        return float(Decimal(yhat) + history[-interval])

    days_in_year = 365
    forecast = model_fit.forecast(steps=14)[0]

    history = [x for x in X]
    day = 1

    for yhat in forecast:
        inverted = inverse_difference(history, yhat, days_in_year)
        print('Day %d: %f' % (day, inverted))
        history.append(inverted)
        day += 1

    return forecast


