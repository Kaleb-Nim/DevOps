import pytest

@pytest.mark.parametrize("filename", ["test.png", "test.jpeg", "test.jpg", "test.gif", "test.pdf"])
def test_upload_file(client, filename):
    with open(filename, "rb") as f:
        data = {"file": (f, filename)} # Change the Data 
        response = client.post("/predict", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully."}

@pytest.mark.parametrize("filename", ["test.gif", "test.pdf"])
def test_upload_invalid_file(client, filename):
    with open(filename, "rb") as f:
        data = {"file": (f, filename)}
        response = client.post("/predict", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid file format. Only .png, .jpeg, and .jpg files are allowed."}
