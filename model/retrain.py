from model_func import preprocess, retrain, model_save, model_load

model = model_load("model.pkl")
X_train, X_test, y_train, y_test = preprocess("data/elementary.csv")
model = retrain(model, X_train, y_train)
model_save(model, "model.pkl")