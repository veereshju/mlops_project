from model_func import preprocess_split, preprocess_scale, train, model_save, model_load
import mlflow
import os

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("param1", 5)


os.makedirs("/mlruns", exist_ok=True)
mlflow.set_tracking_uri("file:///mlruns")
mlflow.set_experiment("Integraion experiment")

X_train, X_test, y_train, y_test = preprocess_split("model/data/elementary.csv")
X_train = preprocess_scale(X_train)
X_test = preprocess_scale(X_test)
model = train(X_train, y_train)
model_save(model, "model/model.pkl")
