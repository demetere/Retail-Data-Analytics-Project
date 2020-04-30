def predict_prophet(model, validation):
    # Create new dataframe with the dates that has to be predicted
    future_dataframe = validation.drop('y', axis=1)

    # Reset index
    future_dataframe = future_dataframe.reset_index(drop=True)

    # Predict
    forecast = model.predict(future_dataframe)

    # Pick only dates and predictions
    forecast = forecast[['ds', 'yhat']]

    # Rename so we understand which one is Date and which one Sale
    forecast = forecast.rename(columns={'ds': 'Date', 'yhat': 'Sale'})

    print(forecast)

    return forecast
