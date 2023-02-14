from application.utilities import load_img, reshape_image,make_prediction
from application import ai_model
from application.models import Entry , EntryCifar
from application.routes import add_to_db, remove_entry
from datetime import datetime
import json
import os
import time
from io import BytesIO
import requests
import base64
import json
import pytest

from application import app

app = app.test_client()


#  ["./tests/upload_test_files/test_image0.png","./tests/upload_test_files/test_image1.png","./tests/upload_test_files/test_image2.png","./tests/upload_test_files/test_image3.png","./tests/upload_test_files/test_image4.png"]
# 4. Ensure classifier results + parameters are added to history
@pytest.mark.parametrize(
    "entrylist",
    [
        ["./tests/upload_test_files/test_image0.png", "plate",0.534123123 ,"fine", "vgg19"],
        ["./tests/upload_test_files/test_image1.png", "maple_tree",0.442132312 ,'fine', "vgg19"],
        ['./tests/upload_test_files/test_image9.png','apple',0.888273612312 ,'fine', 'Cifar100Efficient'],
    ],
)
def test_add_db(client,capsys, entrylist):
    """
    Test if the entry is added to the database
    """
    with client.application.test_request_context():
        with capsys.disabled():
                # Save the prediction to the database
            new_entry = EntryCifar(
                image_path = entrylist[0],
                prediction = entrylist[1],
                prediction_prob = entrylist[2],
                dataset_type = entrylist[3],
                model_name = entrylist[4],
                predicted_on_date = datetime.now()
            )
            print("==>> new_entry: ", new_entry)
            id_added = add_to_db(new_entry)

            # check if database has the entry
            assert id_added is not None
            # remove the entry from the database
            is_deleted = remove_entry(id_added)
            assert is_deleted ==1
