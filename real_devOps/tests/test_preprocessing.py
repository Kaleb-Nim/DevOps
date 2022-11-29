import pytest 

from application.utilities import preProcess, formatPrediction

prediciton_format = {
    "age": 19,
    "bmi": 27.9,
    "children": 0,
    "smoker": "no",
    "sex": "male",
    "region": "southwest",
}

def test_preProcess():
    prediction_input = preProcess(prediciton_format)
    # check if pandas dataframe
    assert type(prediction_input) == "pandas.core.frame.DataFrame"
    # check if the dataframe has 6 columns
    assert len(prediction_input.columns) == 6
    # check 
    assert prediction_input["age"][0] == 19
    assert prediction_input["bmi"][0] == 27.9
    assert prediction_input["children"][0] == 0
    assert prediction_input["smoker"][0] == 0
    assert prediction_input['smoker_yes'] == 0.0
    assert prediction_input['sex_male'] == 1.0
    assert prediction_input['region_northwest'] == 0
    assert prediction_input['region_southeast'] == 0.0
    assert prediction_input['region_southwest'] == 1.0