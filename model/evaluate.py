from model_func import preprocess, model_load, evaluate

def test_performace():
    model = model_load("model.pkl")
    X_train, X_test, y_train, y_test = preprocess("data/trigo.csv")
    mse = evaluate(model, X_test)
    print("Mean Square Error of the model is {}".format(mse))
    assert mse > 0.01