# # 1: Import libraries need for the test
# from application.models import Entry
# import datetime as datetime
# import pytest
# from flask import json

# # Unit Test
# # 2: Parametrize section contains the data for the test
# @pytest.mark.parametrize(
#     "entrylist",
#     [
#         [1.0, 2.1, 1.1, 1.1, 0, 2, 1.0],  # Test integer arguments
#         [0.1, 0.2, 0.3, 0.4, 1, 2, 1.0],  # Test float arguments
#     ],
# )

# # 3: Write the test function pass in the arguments
# def test_EntryClass(entrylist, capsys):
#     with capsys.disabled():
#         print(entrylist)
#         print("==>> entrylist[0]: ", entrylist[0])
#         now = datetime.datetime.utcnow()
#         new_entry = Entry(
#             age=entrylist[0],
#             sex=entrylist[1],
#             bmi=entrylist[2],
#             children=entrylist[3],
#             smoker=entrylist[4],
#             region=entrylist[5],
#             prediction=entrylist[6],
#             predicted_on_date=now,
#         )
#         assert new_entry.age == entrylist[0]
#         assert new_entry.sex == entrylist[1]
#         assert new_entry.bmi == entrylist[2]
#         assert new_entry.children == entrylist[3]
#         assert new_entry.smoker == entrylist[4]
#         assert new_entry.region == entrylist[5]
#         assert new_entry.prediction == entrylist[6]
#         assert new_entry.predicted_on_date == now


# # 4: Expected Failure Testing
# # What if input contains 0 or negative values
# # What if output is negative
# @pytest.mark.xfail(reason="arguments <= 0")
# @pytest.mark.parametrize(
#     "entrylist",
#     [
#         [0, 2, 1, 1, 0],
#         [1, -2, 2, 2, 1],
#         [1, 2, -2, 2, 2],
#         [1, 2, 2, -2, 1],
#         [1, 2, 2, 2, -1],
#     ],
# )
# def test_EntryValidation(entrylist, capsys):
#     test_EntryClass(entrylist, capsys)


# # 5: Test add API
# @pytest.mark.parametrize("entrylist", [[1, 'm', 10,0, 'yes','southwest',1000.0], [1, 'f', 12,0, 'no','southwest',2000.0]])
# def test_addAPI(client, entrylist, capsys):
#     with capsys.disabled():
#             # Format the data
#         prediciton_format = {
#                 'age':entrylist[0],
#                 'sex':entrylist[1],
#                 'bmi':entrylist[2],
#                 'children':entrylist[3],
#                 'smoker':entrylist[4],
#                 'region':entrylist[5],
#                 'prediction':entrylist[6]
#             }
#         # use client object to post
#         # data is converted to json
#         # posting content is specified
#         response = client.post(
#             "/predict",
#             data=json.dumps(prediciton_format),
#             content_type="application/json",
#         )
#         # check the outcome of the action
#         assert response.status_code == 200
#         assert response.headers["Content-Type"] == "application/json"
#         response_body = json.loads(response.get_data(as_text=True))
#         assert response_body["id"]
