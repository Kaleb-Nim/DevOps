# #Unit Testing for Retrieving Entry
# from flask import json
# from application.models import Entry
# import pytest
# from datetime import datetime

# #Test get API
# @pytest.mark.parametrize("entrylist",[
#  [ 1, 10, 'male', 3,'yes', 'southeast',100.1],
#  [ 2,  10, 'male', 4,'yes', 'southeast',100.1]
# ])

# def test_getAPI(client, entrylist, capsys):
#     with capsys.disabled():
#         response = client.get(f'/api/get/{entrylist[0]}')
#         ret = json.loads(response.get_data(as_text=True))
#         #check the outcome of the action
#         assert response.status_code == 200
#         assert response.headers["Content-Type"] == "application/json"
#         response_body = json.loads(response.get_data(as_text=True))
#         assert response_body["age"] == float(entrylist[0])
#         assert response_body["bmi"] == float(entrylist[1])
#         assert response_body["sex"] == (entrylist[2])
#         assert response_body["children"] == float(entrylist[3])
#         assert response_body["smoker"] == (entrylist[4])
#         assert response_body["region"] == (entrylist[5])
#         assert response_body["prediction"] == float(entrylist[6])

# # Test PREDICT API
# @pytest.mark.parametrize("postlist",[
#  [ 40, 'male', 18, 1,'no', 'southeast',4500.1],
#  [ 33, 'female', 20,2 ,'yes', 'southwest',3300.1]
# ])
# def test_deleteAPI(client,postlist,capsys):
#     new_entry = Entry(
#                 age=postlist[0],
#                 sex=postlist[1],
#                 bmi=postlist[2],
#                 children=postlist[3],
#                 smoker=postlist[4],
#                 region=postlist[5],
#                 prediction=postlist[6],
#                 predicted_on_date=datetime.now(),
#             )
#     response = client.post(f'/api/add',data = json.dumps(new_entry),content_type="application/json")
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
