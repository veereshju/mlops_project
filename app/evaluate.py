from model_func import preprocess_split, preprocess_scale, model_load, evaluate

def test_performace():
    model = model_load("model/model.pkl")
    X_train, X_test, y_train, y_test = preprocess_split("model/data/elementary.csv")
    X_train = preprocess_scale(X_train)
    X_test = preprocess_scale(X_test)
    mse = evaluate(model, X_test, y_test)
    print("Mean Square Error of the model is {}".format(mse))
    assert mse < 0.02