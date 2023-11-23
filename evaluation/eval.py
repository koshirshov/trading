from sklearn.metrics import mean_absolute_error

def get_evaluation(predict, target, open_prices, order_price):
    mae = mean_absolute_error(predict, target)
    print(f'mae is {mae}')
    n_orders = predict.shape[0]
    buy = average_order/open_prices
    sell = buy/open_prices
    ### tbd