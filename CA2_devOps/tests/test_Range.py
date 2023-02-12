"""
Inputs or data that are not in the range of accepted values should be rejected
"""

import pytest
from application.utilities import preProcess
from application import ai_model
from application.models import Entry
from application.routes import add_to_db
import datetime
import json 

# 1. Ensures form input, negative integers for Age, BMI and No. children are rejected
@pytest.mark.parametrize(
    "entrylist",
    [
        [-22, "male", -15, 0, "yes", "southwest"],
        [-33, "female", -17, -2, "no", "northeast"],
    ],
)
def test_negative_entry(client, entrylist, capsys):
    with capsys.disabled():
        #prepare the data into a dictionary
        prediciton_format = {
                "age": entrylist[0],
                "sex": entrylist[1],
                "bmi": entrylist[2],
                "children": entrylist[3],
                "smoker": entrylist[4],
                "region": entrylist[5],
        }
        #use client object to post
        #data is converted to json
        #posting content is specified
        response = client.post('/predict', 
        data=json.dumps(prediciton_format),
        content_type="application/json",)
        # Check if flash message is displayed
        #check the outcome of the action
        assert response.status_code != 400
        response_body = json.loads(response.get_data(as_text=True))
        print("==>> response_body: ", response_body)
        assert response_body["id"]

