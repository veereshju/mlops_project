import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import pickle
from mlflow.models import infer_signature

def preprocess_split(path):
    dataset = pd.read_csv(path)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    return train_test_split(X, y)


def preprocess_first_scale(X_train, X_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    with open('model/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    X_test = scaler.transform(X_test)
    return X_train, X_test


def preprocess_scale(X_test):
    scaler = StandardScaler()
    with open('model/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    X_test = scaler.transform(X_test)
    return X_test

def train(model, X_train, y_train):
    model.fit(X_train, y_train)
    train_acc = model.score(X_train, y_train)
    mlflow.log_metric("Training Accuracy", train_acc)
    print(f"Train Accuracy: {train_acc:.3%}")

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    r2 =  r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mean_squared_error", mse)
    return r2, mse

def retrain(model, X_train, y_train):
    model.partial_fit(X_train, y_train)

def model_save(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def model_load(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

def mlflow_run(model, name, path, params):
    with mlflow.start_run(run_name=name):
        X_train, X_test, y_train, y_test = preprocess_split(path)
        X_train, X_test = preprocess_first_scale(X_train, X_test)
        train(model, X_train, y_train)
        r2, mse = evaluate(model, X_test, y_test)
        mlflow.log_params(params)
        mlflow.set_tag("Training Info", "Regression model for integration data")
        signature = infer_signature(X_train, model.predict(X_train))
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=name,
            signature=signature,
            input_example=X_train,
            registered_model_name=name,
        )
    return model_info, r2