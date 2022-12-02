"""
Consistency Testing: Application should respond identically for the same inputs or data sent
"""

import pytest
from application.utilities import preProcess
from application import ai_model
from application.models import Entry
from application.routes import add_to_db
import datetime


# 2: Prediction cost same when same data sent multiple times
def test_consistentPrediction():
    """
    Test the prediction is consistent
    """
    prediciton_format = {
        "age": 19,
        "bmi": 27.9,
        "children": 0,
        "smoker": "no",
        "sex": "male",
        "region": "southwest",
    }
    prediciton_format3 ={
        "age": 33,
        "bmi": 27.9,
        "children": 0,
        "smoker": "yes",
        "sex": "female",
        "region": "northwest" 
    }
    prediction_input = preProcess(prediciton_format)
    # same input should have same prediction
    preduction_input2 = preProcess(prediciton_format) # same as prediction_input
    # different input should have different prediction
    prediction_input3 = preProcess(prediciton_format3)


    prediction = ai_model.predict(prediction_input)
    prediction2 = ai_model.predict(preduction_input2)
    prediction3 = ai_model.predict(prediction_input3)

    # check if the prediction is consistent
    assert prediction == prediction2
    # check if the prediction is different
    assert prediction != prediction3
    