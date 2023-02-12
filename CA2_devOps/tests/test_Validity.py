"""
Validity Testing: Test that the application works as intended on real data
"""

import pytest
from application.utilities import preProcess
from application import ai_model
from application.models import Entry
from application.routes import add_to_db
from datetime import datetime

# 1. Ensure all valid GET requests return 200
@pytest.mark.parametrize(
    "endpoint",
    [
        ("forms", 200),
        ("history", 200),
        ("", 200),
        ("home", 200),
    ],
)
def test_route_codes(client, endpoint, capsys):
    with capsys.disabled():
        endpoint, code = endpoint[0], endpoint[1]
        response = client.get(f"/{endpoint}")
        assert response.status_code == code

# 2. Ensure data preprocessing (one-hot-encode + scaling) for predictive model is correct
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

# 3. Ensure model able to perform prediction from form data
@pytest.mark.parametrize(
    "entrylist",
    [
        [22, "male", 15, 0, "yes", "southwest"],
        [33, "female", 17, 2, "no", "northeast"],
    ],
)
def test_predict(client,capsys, entrylist):
    """
    Test the predict function in ai_model.py, which is used to predict the insurance cost
    """
    with capsys.disabled():
        # Format the data
        prediciton_format = {
                "age": entrylist[0],
                "sex": entrylist[1],
                "bmi": entrylist[2],
                "children": entrylist[3],
                "smoker": entrylist[4],
                "region": entrylist[5],
        }
        prediction_input = preProcess(prediciton_format)
        # Predict the cost
        prediction = ai_model.predict(prediction_input)

        # Check if the prediction is a number
        assert isinstance(prediction[0], float)
        # Check if the prediction is positive
        assert prediction[0] > 0
        # Check if the prediction is not too high
        assert prediction[0] < 1000000

# 4. Ensure model results + parameters are added to history
@pytest.mark.parametrize(
    "entrylist",
    [
        [22, "male", 15, 0, "yes", "southwest", 4350.51],
        [33, "female", 17, 2, "no", "northeast",14231.51],
        [18,'male', 25, 0, 'no', 'northeast', 1725.55],
    ],
)
def test_add_db(client,capsys, entrylist):
    """
    Test the predict function in ai_model.py, which is used to predict the insurance cost
    """
    with capsys.disabled():
            # Save the prediction to the database
        new_entry = Entry(
                age=entrylist[0],
                sex=entrylist[1],
                bmi=entrylist[2],
                children=entrylist[3],
                smoker=entrylist[4],
                region=entrylist[5],
                prediction=entrylist[6],
                predicted_on_date= datetime.now(),
            )
        print("==>> new_entry: ", new_entry)
        id_added = add_to_db(new_entry)

        # check if database has the entry
        assert Entry.query.filter_by(id=id_added).first() is not None

