import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, StandardScaler ,OneHotEncoder,FunctionTransformer , MinMaxScaler
import pickle
df_raw = pd.read_csv('application/static/insurance.csv')

from sklearn.preprocessing import OneHotEncoder

 #AI model file
joblib_file = "application/static/Pickle_RL_Model.pkl"
# Load from file
with open(joblib_file, 'rb') as f:
    ai_model = pickle.load(f)

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
    return df_final


# prediciton_format = {
#     'age':1,
#     'sex':'male',
#     'bmi':1,
#     'children':1,
#     'smoker':'no',
#     'region':'southwest',
# }

# preduction_input = preProcess(prediciton_format)
# print("==>> preduction_input: ", preduction_input.head())
# prediction = ai_model.predict(preduction_input)
# print("==>> prediction: ", prediction)
