import pandas as pd

feature_list = ['Open', "High", "Low", "Close", "Volume", "price_diff1", "price_diff2", "price_diff3", "price_diff4"]
drop_list = ["High", "Low", "Close", "Volume", "price_diff1", "price_diff2", "price_diff3", "price_diff4"]
target = ['target']
prices_features = ['open', 'high', 'low', 'close']
time_features = ['hour', 'day', 'day_of_week', 'month', 'year']
other_features = ['volume']
diff_features = ['price_diff1', 'price_diff2', 'price_diff3', 'price_diff4']

def generate_extra_features(data):
    data['price_diff1'] = data['High'] - data['Open']
    data['price_diff2'] = data['High'] - data['Low']
    data['price_diff3'] = data['Low'] - data['Open']
    data['price_diff4'] = data['Close'] - data['Open']
    #data['avg_vol'] = data['volume']/data['Num_trades']

    return data
    
def create_features_from_previos_n_min(data, n_minutes_before):
    """data is increasing by timestamp"""
    for i in range(1, n_minutes_before):
        for feature in feature_list:
            data[f'{feature}_{i}min_before'] = data[feature].shift(i)
    data = data.dropna()

    return data

def add_time_features(data):
    data = data.set_index('Timestamp')
    data.index = pd.to_datetime(data.index)
    data = (
        data
        .assign(minute = data.index.minute)
        .assign(hour = data.index.hour)
        .assign(day = data.index.day)
        .assign(month = data.index.month)
        .assign(week_of_year = data.index.week)
        .assign(year = data.index.year)
        )
    data.drop(columns=["week_of_year", "Date", "Time"], inplace=True)
    data['year'] -= 2022

    return data
    
def devide_data_for_train_and_val(data, target, n_to_val):
    data_train = data.iloc[:n_to_val]
    target_train = target.iloc[:n_to_val]
    data_val = data.iloc[-n_to_val:]
    target_val = target.iloc[-n_to_val:]

    return data_train, target_train, data_val, target_val

def data_prepare(n_minutes_before, n_to_val):
    """
    create dataset with features from initial csv's
    """
    data = pd.read_csv('./data/btc_data.csv')
    data = add_time_features(data)
    data = generate_extra_features(data)
    data = create_features_from_previos_n_min(data, n_minutes_before)

    target = data['Close'].copy(deep=True)
    data = data.drop(columns=drop_list)

    return devide_data_for_train_and_val(data, target, n_to_val)
