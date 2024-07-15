from model_func import preprocess_split, preprocess_scale, train, model_save, model_load

X_train, X_test, y_train, y_test = preprocess_split("model/data/trigo.csv")
X_train = preprocess_scale(X_train)
X_test = preprocess_scale(X_test)
model = train(X_train, y_train)
model_save(model, "model/model.pkl")
model = model_load("model/model.pkl")