from model_func import preprocess_split, preprocess_scale, train, model_save, model_load, evaluate, preprocess_first_scale
import mlflow
import os
from sklearn.linear_model import SGDRegressor
from mlflow.models import infer_signature
from sklearn.svm import SVR

#os.makedirs("/mlruns", exist_ok=True)
#mlflow.set_tracking_uri("file:///mlruns")
mlflow.set_tracking_uri("http://127.0.0.1:8000")
mlflow.set_experiment("Integraion experiment")

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

sgd_params = {
    "max_iter": 1000,
    "loss": "squared_error",
    "penalty": "l2",
    "eta0": 0.01,
    "tol": 1e-3,
    "random_state": 42,
}

scores = list()
infos = list()

sgd = SGDRegressor(**sgd_params)

info_sgd, r2 = mlflow_run(sgd, "sgd_regressor", "model/data/elementary.csv", sgd_params)
scores.append(r2)
infos.append(info_sgd)

svr_params = {
    "kernel":'rbf',
    "degree":3,
}
deg = [2, 3, 4, 5]

for i in deg:
    svr_params["degree"] = i
    svr = SVR(**svr_params)
    info_svr, r2 = mlflow_run(svr, "svr_regressor with degree {}".format(str(i)), "data/trigo.csv", svr_params)
    scores.append(r2)
    infos.append(info_svr)

uri_of_model = infos[scores.index(max(scores))].model_uri

loaded_model = mlflow.pyfunc.load_model(uri_of_model)

model_save(loaded_model, "model/model.pkl")
