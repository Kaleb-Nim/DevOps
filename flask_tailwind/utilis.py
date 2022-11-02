import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, StandardScaler ,OneHotEncoder,FunctionTransformer , MinMaxScaler
import pickle

# load model
Pkl_Filename = "../Pickle_RL_Model.pkl"  

with open(Pkl_Filename, 'rb') as file:  
    model = pickle.load(file)


df_raw = pd.read_csv('../insurance.csv')
# json = {
#     "age": 1,
#     "bmi": 0.4,
#     "children": 0.6,
#     "sex":"Male",
#     "smoker":"Non-smoker",
#     "region": "Southeast"
# }
from sklearn.preprocessing import OneHotEncoder
 

def preProcess(json_data,main_df=df_raw):
    '''
    This function takes in a single json object as input (with all features)
    (Input must follow specific ordering)
    Performs data preprocessing which includes:
    - One hot encoding
    - Scaling
    Returns a single row dataframe with all features for prediction
    '''
    print("json_Data==>", json_data,type(json_data))
    # # convert value in json_data to float 
    # for key in json_data:
    #     if key in ['age','bmi','children']:
    #         json_data[key] = float(json_data[key])
    # print("json_Data converted==>", json_data,type(json_data))

    # Create a single row dataframe from the json object
    df = pd.DataFrame(json_data,index=[0])

    # Extract all numeric values
    numeric = df.select_dtypes(include=['number']).columns.tolist()
    print("==>> numeric: ", numeric)

    # Scale numeric values
    scaler = StandardScaler()
    df_scaled = df.copy()
    scaler.fit(main_df[numeric])
    df_scaled[numeric] = scaler.transform(df_scaled[numeric])
    print("==>> df_scaled[numeric]: ", df_scaled[numeric])
    
    # One hot encode categorical values
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()
    print("==>> categorical: ", categorical)

    # one hot encode categorical values
    ohe = OneHotEncoder(sparse=False,handle_unknown='ignore',drop='first')
    ohe.fit(main_df[categorical])

    df_ohe = pd.DataFrame(ohe.transform(df[categorical]),columns=ohe.get_feature_names_out(categorical))
    # Concatenate the scaled numeric and one hot encoded categorical values
    df_final = pd.concat([df_scaled[numeric],df_ohe],axis=1)
    
    # Return the final dataframe and original dataframe
    return df_final, df


def format(age,bmi,children,sex,smoker,region):
    '''
    This function takes in all the features as input 
    Returns 
    1. a json object with all features
    2. List format to save in database 
    '''
    prediction = {
            "age": age,
            "bmi": bmi,
            "children": children,
            "sex":sex,
            "smoker": smoker,
            "region": region,
        }
    # Return a json object for prediction 
    return prediction, list(prediction.values())

# age = 2
# bmi = 0.4
# children = 0.8
# sex = 'male'
# smoker = 'no'
# region = 'southeast'
# prediction,history = format(age,bmi,children,sex,smoker,region)
# print("==>> type(prediction): ", type(prediction))
# print("==>> prediction: ", prediction)

# prediction_input,history = preProcess(prediction)
# print("==>> type(prediction_input): ", type(prediction_input))


# # Predict
# print("==>> type(model): ", type(model))
# prediction = model.predict(prediction_input)


# output = prediction[0]
# print(output)