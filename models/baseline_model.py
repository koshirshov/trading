class BaselineModel:

    def __init__(self):
        pass

    def fit(self, X_train=None, y_train=None):
        pass
    
    def predict(self, X):
        return X["Close_1min_before"]