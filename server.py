import numpy as np
from flask import Flask, request, jsonify
import pickle
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder, StandardScaler ,OneHotEncoder,FunctionTransformer , MinMaxScaler
from utilis import preProcess
from joblib import load

app = Flask(__name__)

model = load('model.pkl')

@app.route('/api',methods=['POST'])
def predict():
    """
    Takes an json input and uses model (a trained Regression model ) to make a
    prediction.

    Returns:
     prediction coefficient 
     
     pred_conf (model confidence)
    """
    jsonData = request.get_json(silent = True)
    # Convert jsonData to a single row dataframe
    prediction_input, original_input = preProcess(jsonData)

    if jsonData is None:
        return 'No data'
    else:
        prediction = model.predict(prediction_input)
        output = prediction[0]
    return output, dict(original_input)


if __name__ == '__main__':
    app.run(port=5000, debug=True)