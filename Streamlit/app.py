import os
import json
import requests
import streamlit as st
import tensorflow as tf
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import time
import base64
from pathlib import Path
import numpy as np

### Streamlit code (works as a straigtht-forward script) ###
st.title("Welcome to Kaleb's DevOps CA1 Assignment ​🧑‍⚕️​🩺​")
st.header("Predict insurance costs using a Regression model based on individuals' personal attributes such as `age` , `bmi` and `smoking` ")

# Pick the model version
choose_model = st.sidebar.selectbox(
    "Pick model you'd like to use",
    ("Model 1: RandomForestRegressor ", # original 10 classes
     "Model 2 ( Comming soon )", # original 10 classes + donuts
     "Model 3 ( Comming soon )") # 11 classes (same as above) + not_food class
)

age = st.number_input('What is your Age',min_value=0, max_value=125, value=0, step=1)

bmi = st.number_input('What is your BMI',min_value=0.0, max_value=100.0, value=0.0, step=0.1)

isSmoker = st.selectbox(
'Are u a smoker?',
('no', 'yes'))

gender = st.selectbox(
    'What is your gender',
    ('male','female')
)

region = st.selectbox(
    'What is your region',
    ('northwest','northeast','southeast','southwest') #
)

st.write('You selected:', age, bmi, isSmoker,gender,region)

# session_state = st.session_state.get(pred_button = False)

pred_button = st.button("Predict")

prediction = (
    0.1,
    0.4,
    0.6,
    0,
    1,
    1,
    0,
    0
)

df = pd.DataFrame(
   np.random.randn(10, 5),
   columns=('col %d' % i for i in range(5)))

# Did the user press the predict button?
data = ()
if pred_button:
    st.table(df)

