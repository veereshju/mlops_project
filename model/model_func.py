import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
import pickle
from sklearn.metrics import mean_squared_error

def preprocess(path):
    dataset = pd.read_csv(path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def train(X_train, y_train):
    model = SGDRegressor(max_iter=1000, tol=1e-3, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate(model, X_test, y_test):
    return mean_squared_error(y_test, model.predict(X_test))

def retrain(model, X_train, y_train):
    model.partial_fit(X_train, y_train)

def predict(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred

def model_save(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def model_load(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model