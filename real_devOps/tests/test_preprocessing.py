import pytest

from application.utilities import preProcess
from application import ai_model

# 1: Test preprocessing
def test_preProcess():
    """
    Test the preProcess function in utilities.py, which is used to preprocess the data before prediction
    pre process includes one hot encoding and scaling
    """
    prediciton_format = {
        "age": 19,
        "bmi": 27.9,
        "children": 0,
        "smoker": "no",
        "sex": "male",
        "region": "southwest",
    }
    prediction_input = preProcess(prediciton_format)

    # check if the dataframe has 8 columns
    assert len(prediction_input.columns) == 8
    # check if have correct columns
    assert "age" in prediction_input.columns
    assert "bmi" in prediction_input.columns
    assert "children" in prediction_input.columns
    assert "smoker_yes" in prediction_input.columns
    assert "sex_male" in prediction_input.columns
    assert "region_southwest" in prediction_input.columns
    assert "region_northwest" in prediction_input.columns
    assert "region_southeast" in prediction_input.columns
    # check if the numeric values are scaled
    assert prediction_input["age"].max() <= 1
    assert prediction_input["bmi"].max() <= 1
    assert prediction_input["children"].max() <= 1

# 2: Test consistent prediction
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
    