import pytest
from application.utilities import preProcess
from application import ai_model
from application.models import Entry
from application.routes import add_to_db
from datetime import datetime
import json
import os
import time
from io import BytesIO


class_list = ("Flowers", "household_electrical_devices", "People", "Reptile", "vehicels_1")

# Test predict API
@pytest.mark.parametrize(
    "emotionImg", [f"{e}.{ext}" for e in class_list for ext in ["png", "jpg"]]
)
def test_predAPI(client, emotionImg, capsys):
    with capsys.disabled():

        time.sleep(3)

        data = {
            "file": (
                BytesIO(open(f"./tests/test_files/{emotionImg}", "rb").read()),
                emotionImg,
            )
        }

        response = client.post(
            "/forms/upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))

        # Remove test api images
        os.remove(f"./application/static/images/{response_body['file_path']}")
        assert "error" not in response_body.keys()

        assert (
            emotionImg.split(".")[0].capitalize()
            in np.array(response_body["prediction"])[:, 0][:4]
        )


# Test non png or non jpg files
@pytest.mark.xfail(reason="Not png or jpg")
@pytest.mark.parametrize("files", ["angry.txt", "emotion.pdf", "happy.webp"])
def test_predAPI_NonImg(client, files, capsys):
    test_predAPI(client, files, capsys)