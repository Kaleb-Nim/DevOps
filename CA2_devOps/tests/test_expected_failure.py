import pytest

import json
#4: Expected Failure Testing

# 1. Ensures login rejects if username or password is incorrect
# 2: Parametrize section contains the data for the test
# @pytest.mark.parametrize(
#     "loginlist",
#     [
#         ['kaleb.nim@gmail.com',123],  # Test vaild email + password arguments
#         ['sohhongyu@gmail.com',123],  
#     ],
# )
# # 3: Write the test function pass in the arguments
# def test_LoginClass(client,loginlist, capsys):
#     with capsys.disabled():
#         login = {
#             "email": loginlist[0],
#             "password": loginlist[1],
#         }
#         response = client.post('/login', 
#         data=json.dumps(login),
#         content_type="application/json",)

#         assert response.status_code == 200
#         response_body = json.loads(response.get_data(as_text=True))



# 2. Ensures login authentication fails when username and password is incorrect
# What if login is not registered?
@pytest.mark.xfail(reason="invalid login credentials")
@pytest.mark.parametrize(
    "entrylist",
    [
        ["Random@gmail.com",444],
        ['iloveDevOps@gmail.com',333],
        ['ilovePytest@gmail.com',222]
    ],
)
def test_EntryValidation(client,entrylist, capsys):
    with capsys.disabled():
        login = {
            "email": entrylist[0],
            "password": entrylist[1],
        }
        response = client.post('/login', 
        data=json.dumps(login),
        content_type="application/json",)

        assert response.status_code == 200
        response_body = json.loads(response.get_data(as_text=True))    
