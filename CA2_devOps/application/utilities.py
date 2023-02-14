import pandas as pd
from sklearn.preprocessing import (
    OrdinalEncoder,
    StandardScaler,
    OneHotEncoder,
    FunctionTransformer,
    MinMaxScaler,
)
import pickle
import numpy as np

df_raw = pd.read_csv("application/static/insurance.csv")
from PIL import Image
import base64
import json
from sklearn.preprocessing import OneHotEncoder
import requests
from skimage.transform import resize


def load_img(image_path):
    """
    This function takes in a single image path as input
    loads image as a numpy array of size (32, 32, 3) and returns the image
    """
    image = np.array(Image.open(image_path))
    print(f"image is of shape {image.shape}")
    try:
        assert image.shape == (32, 32, 3)
        print(f"image is of shape {image.shape}")
    except AssertionError:
        print("Image shape is not (32, 32, 3)")
        image = reshape_image(image)

    try:
        assert image.shape == (32, 32, 3)
        print(f"image is of shape {image.shape}")
    except AssertionError:
        print("Image shape is still not (32, 32, 3)")

    return image


def reshape_image(test_image):
    """
    This function takes in a single image as input
    Resize the image to (32,32,3) cifar100 and returns the reshaped image
    """
    # resize image to (32,32,3)
    test_image = Image.fromarray(test_image)
    test_image = test_image.resize((32, 32))
    test_image = np.array(test_image)

    resized_test_image = resize(test_image, (32, 32, 3), anti_aliasing=True)
    # expand the dimension of the image to (1, 32, 32, 3)
    resized_test_image = np.expand_dims(resized_test_image, axis=0)
    return resized_test_image


def make_prediction(test_image):
    """
    params:
        image: numpy array of shape (32,32,3)
    Calls API to get prediction
    Returns the prediction

    """
    url = "https://vgg-19-cifar100-model.onrender.com/v1/models/VGG19_cifar100_classifier:predict"
    fine_labels = [
        "apple",
        "aquarium_fish",
        "baby",
        "bear",
        "beaver",
        "bed",
        "bee",
        "beetle",
        "bicycle",
        "bottle",
        "bowl",
        "boy",
        "bridge",
        "bus",
        "butterfly",
        "camel",
        "can",
        "castle",
        "caterpillar",
        "cattle",
        "chair",
        "chimpanzee",
        "clock",
        "cloud",
        "cockroach",
        "couch",
        "crab",
        "crocodile",
        "cup",
        "dinosaur",
        "dolphin",
        "elephant",
        "flatfish",
        "forest",
        "fox",
        "girl",
        "hamster",
        "house",
        "kangaroo",
        "keyboard",
        "lamp",
        "lawn_mower",
        "leopard",
        "lion",
        "lizard",
        "lobster",
        "man",
        "maple_tree",
        "motorcycle",
        "mountain",
        "mouse",
        "mushroom",
        "oak_tree",
        "orange",
        "orchid",
        "otter",
        "palm_tree",
        "pear",
        "pickup_truck",
        "pine_tree",
        "plain",
        "plate",
        "poppy",
        "porcupine",
        "possum",
        "rabbit",
        "raccoon",
        "ray",
        "road",
        "rocket",
        "rose",
        "sea",
        "seal",
        "shark",
        "shrew",
        "skunk",
        "skyscraper",
        "snail",
        "snake",
        "spider",
        "squirrel",
        "streetcar",
        "sunflower",
        "sweet_pepper",
        "table",
        "tank",
        "telephone",
        "television",
        "tiger",
        "tractor",
        "train",
        "trout",
        "tulip",
        "turtle",
        "wardrobe",
        "whale",
        "willow_tree",
        "wolf",
        "woman",
        "worm",
    ]

    print("==>> test_image: ", test_image)
    print("==>> test_image.shape: ", test_image.shape)
    data = json.dumps(
        {"signature_name": "serving_default", "instances": test_image.tolist()}
    )  # see [C]
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    print(f"json_response: {json_response}")
    predictions = json.loads(json_response.text)['predictions']
    print(f"these are the predictions: {predictions}")
    
    # Map the predictions to the fine labels
    predicted_labels = [fine_labels[np.argmax(pred)] for pred in predictions]
    print(f"these are the predicted labels: {predicted_labels[0]}")
    return predicted_labels[0]
