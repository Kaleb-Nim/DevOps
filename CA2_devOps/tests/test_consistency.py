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

# 2: Prediction cost same when same data sent multiple times
def test_consistentPrediction(client):
   test_image1_path = "./tests/upload_test_files/test_image9.png"
   test_image2_path = "./tests/upload_test_files/test_image8.png"
   # Load the image
   image1 = load_img(test_image1_path)
   image2 = load_img(test_image2_path)
   predictions1,predicted_labels_prob1 = make_prediction(image1,model_name="vgg19")
   # Assign different variable name to the prediction of the same image
   predictions1_1,predicted_labels_prob1_1 = make_prediction(image1,model_name="vgg19")
    # different prediction for different image
   predictions2,predicted_labels_prob2 = make_prediction(image2,model_name="vgg19")

   # check if the prediction is consistent
   assert predictions1 == predictions1_1 # should be same prediction for same image
   # check if the prediction is different
   assert predictions1 != predictions2
