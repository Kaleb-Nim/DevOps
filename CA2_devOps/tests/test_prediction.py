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
# from tensorflow.keras.datasets.cifar100 import load_data

# # load dataset for 20 Superclass 
# (X_train, y_train), (X_test, y_test) = load_data(label_mode="coarse")

# # summarize loaded dataset
# print('Train: X=%s, y=%s' % (X_train.shape, y_train.shape))
# print('Test: X=%s, y=%s' % (X_test.shape, y_test.shape))

# # load 10 images from the test dataset
# test_image = X_test[:10]

# # Save these 10 images to upload_test_files folder
# from matplotlib import image
# for i in range(10):
#    image.imsave(f'./tests/upload_test_files/test_image{i}.png',test_image[i])

# Load the image
image = load_img('./tests/upload_test_files/test_image0.png')

# Predict the class of an image
def test_prediction():
   predictions = make_prediction(image)
   # Check that the prediction is a string
   assert isinstance(predictions, str)


# Test if model is hosted and running
@pytest.mark.parametrize(
    "model_API", ["https://vgg-19-cifar100-model.onrender.com/v1/models/VGG19_cifar100_classifier"] # Add second model API here
)
def test_model_hosted(client,model_API):
   print(f'model_API: {model_API}')
   # Get the prediction from the model
   response = requests.get(model_API)
   # Check that the response is 200
   assert response.status_code == 200

