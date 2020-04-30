def predict(model, customers_copy):
    prediction = model.predict(customers_copy.drop('NextPurchaseDayRange', axis=1))

    # Customers who will repurchase within 14 days
    repurchase_customers = []

    for i in range(0, len(prediction)):
        if prediction[i] == 1:
            repurchase_customers.append(customers_copy.columns[i])
    print('Customers Who will repurchase: ')
    print("\n".join(repurchase_customers))
    return repurchase_customers