# Unit Testing for Retrieving Entry
from flask import json
from application.models import Entry
import pytest
from datetime import datetime
from application.utilities import preProcess
from application import ai_model
# 1: Test POST API
@pytest.mark.parametrize(
    "entrylist",
    [
        [22, "male", 15, 0, "yes", "southwest"],
        [1, "female", 12, 0, "no", "northeast"],
    ],
)
def test_addAPI(client, entrylist, capsys):
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
        # use client object to post
        # data is converted to json
        # posting content is specified

        response = client.post(
            "/predict",
            data=json.dumps(prediciton_format),
            content_type="application/json",
        )
        # check the outcome of the action
        assert response.status_code == 200
        response_body = json.loads(response.get_data(as_text=True))
        print("==>> response_body: ", response_body)
        assert response_body["id"]


# Test get API
@pytest.mark.parametrize(
    "entrylist",
    [
        [1, 10, "male", 3, 1, "yes", "southeast", 100.1],
        [2, 10, "male", 4, 2, "yes", "southeast", 100.1],
    ],
)
def test_getAPI(client, entrylist, capsys):
    with capsys.disabled():
        response = client.get(f"/api/get/{entrylist[0]}")
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == entrylist[0]
        assert response_body["age"] == float(entrylist[1])
        assert response_body["sex"] == (entrylist[2])
        assert response_body["bmi"] == float(entrylist[3])
        assert response_body["children"] == float(entrylist[4])
        assert response_body["smoker"] == (entrylist[5])
        assert response_body["region"] == (entrylist[6])
        assert response_body["prediction"] == float(entrylist[7])


# # Test delete API
# @pytest.mark.parametrize(
#     "postlist",
#     [
#         [40, "male", 18, 1, "no", "southeast", 4500.1],
#         [33, "female", 20, 2, "yes", "southwest", 3300.1],
#     ],
# )
# def test_deleteAPI(client, postlist, capsys):
#     new_entry = Entry(
#         age=postlist[0],
#         sex=postlist[1],
#         bmi=postlist[2],
#         children=postlist[3],
#         smoker=postlist[4],
#         region=postlist[5],
#         prediction=postlist[6],
#         predicted_on_date=datetime.now(),
#     )
#     response = client.post(
#         f"/api/add", data=json.dumps(new_entry), content_type="application/json"
#     )
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/json"
#     response_body = json.loads(response.get_data(as_text=True))
#     assert response_body["id"]
#     assert response_body["age"] == float(postlist[0])

#     responseDelete = client.delete(f'/api/delete/{response_body["id"]}')
#     assert responseDelete.status_code == 200
#     assert responseDelete.headers["Content-Type"] == "application/json"
#     responseDelete_body = json.loads(responseDelete.get_data(as_text=True))
#     assert responseDelete_body["result"] == "ok"


# # Test POST API
