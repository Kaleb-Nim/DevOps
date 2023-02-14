from application.utilities import load_img, reshape_image,make_prediction
from application import ai_model
from application.models import Entry
from application.routes import add_to_db
from datetime import datetime
import json
import os
import time
from io import BytesIO
import requests
import base64
import json
import pytest

#1. Predict the class of cifar100 image for vgg19 model
@pytest.mark.parametrize(
    "test_image_paths", ["./tests/upload_test_files/test_image0.png","./tests/upload_test_files/test_image1.png","./tests/upload_test_files/test_image2.png","./tests/upload_test_files/test_image3.png","./tests/upload_test_files/test_image4.png"] # Add second model API here
)
def test_prediction(client,test_image_paths):
   # Load the image
   image = load_img(test_image_paths)
   predictions,predicted_labels_prob = make_prediction(image,model_name="vgg19")
   # Check that the prediction is a string
   assert isinstance(predictions, str)
   # Check that the predicted_labels_prob 

#1.2 Predict the class of cifar100 image for Cifar100Efficient model
@pytest.mark.parametrize(
    "test_image_paths", ["./tests/upload_test_files/test_image0.png","./tests/upload_test_files/test_image1.png","./tests/upload_test_files/test_image2.png","./tests/upload_test_files/test_image3.png","./tests/upload_test_files/test_image4.png"] # Add second model API here
)
def test_prediction(client,test_image_paths):
   # Load the image
   image = load_img(test_image_paths)
   predictions,predicted_labels_prob = make_prediction(image,model_name="Cifar100Efficient")
   # Check that the prediction is a string
   assert isinstance(predictions, str)
   # Check that the predicted_labels_prob 


# 2. Test if model is hosted and running
@pytest.mark.parametrize(
    "model_API", ["https://vgg-19-cifar100-model.onrender.com/v1/models/VGG19_cifar100_classifier",'https://efficientnet-cifar100-model.onrender.com/v1/models/Cifar100Efficient'] # Add second model API here
)
def test_model_hosted(client,model_API):
   print(f'model_API: {model_API}')
   # Get the prediction from the model
   response = requests.get(model_API)
   # Check that the response is 200
   assert response.status_code == 200

