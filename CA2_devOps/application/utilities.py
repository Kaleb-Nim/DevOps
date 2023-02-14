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
import cv2

def load_img(image_path):
    """
    This function takes in a single image path as input
    loads image as a numpy array of size (32, 32, 3) and returns the image
    """
    # load image as a numpy array with 3 channels

    image = cv2.imread(image_path)
    # image = np.array(Image.open(image_path))
    print(f"image is of shape {image.shape}")

    resized_image = reshape_image(image)
    return resized_image


def reshape_image(test_image):
    """
    This function takes in a single image as input
    Resize the image to (32,32,3) cifar100 and returns the reshaped image
    """
    # resize image to (32,32,3)
    resized_test_image = cv2.resize(test_image, (32,32), interpolation = cv2.INTER_AREA)

    # expand the dimension of the image to (1, 32, 32, 3)
    resized_test_image = np.expand_dims(resized_test_image, axis=0)
    return resized_test_image


def make_prediction(test_image,model_name):
    """
    params:
        image: numpy array of shape (32,32,3)
    Calls API to get prediction
    Returns the prediction

    """
    print(f'Model name: {model_name}')
    if model_name == "vgg19":
        url = "https://vgg-19-cifar100-model.onrender.com/v1/models/VGG19_cifar100_classifier:predict"
    elif model_name == "Cifar100Efficient":
        url = 'https://efficientnet-cifar100-model.onrender.com/v1/models/Cifar100Efficient:predict'
    else:
        raise ValueError("model_name must be either vgg19 or Cifar100Efficient")

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
    # 20 Super Classes labels
    corse_labels = [
        "aquatic_mammals",
        "fish",
        "flowers",
        "food_containers",
        "fruit_and_vegetables",
        "household_electrical_devices",
        "household_furniture",
        "insects",
        "large_carnivores",
        "large_man-made_outdoor_things",
        "large_natural_outdoor_scenes",
        "large_omnivores_and_herbivores",
        "medium_mammals",
        "non-insect_invertebrates",
        "people",
        "reptiles",
        "small_mammals",
        "trees",
        "vehicles_1",
        "vehicles_2",
    ]
    print("==>> test_image: ", test_image)
    print("==>> test_image.shape: ", test_image.shape)
    data = json.dumps(
        {"signature_name": "serving_default", "instances": test_image.tolist()}
    )  # see [C]
    headers = {"content-type": "application/json"}
    print(f'==> url: {url}')
    json_response = requests.post(url, data=data, headers=headers)
    print(f"json_response: {json_response}")
    predictions = json.loads(json_response.text)['predictions']
    print(f"these are the predictions: {predictions}")
    
    # Map the predictions to the fine labels
    predicted_labels = [fine_labels[np.argmax(pred)] for pred in predictions]
    print(f"these are the predicted labels: {predicted_labels[0]}")
    # Return probability of the predicted label
    print(f"these are the probabilities: {predictions[0][np.argmax(predictions)]}")
    predicted_labels_prob = predictions[0][np.argmax(predictions)]

    # Return top 5 predictions with their probabilities
    top_5 = np.argsort(predictions[0])[-5:][::-1]
    print(f"these are the top 5 predictions: {top_5}")
    top_5_labels = [fine_labels[i] for i in top_5]
    print(f"these are the top 5 labels: {top_5_labels}")
    top_5_probs = [predictions[0][i] for i in top_5]
    print(f"these are the top 5 probabilities: {top_5_probs}")
    
    return predicted_labels[0] , predicted_labels_prob
