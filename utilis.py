import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, StandardScaler ,OneHotEncoder,FunctionTransformer , MinMaxScaler

df = pd.read_csv('insurance.csv')
json = {
    "age": 1,
    "bmi": 0.4,
    "children": 0.6,
    "sex":"Male",
    "smoker":"Non-smoker",
    "region": "Southeast"
}
from sklearn.preprocessing import OneHotEncoder
 

def preProcess(json_data,main_df=df):
    '''
    This function takes in a single json object as input (with all features)
    (Input must follow specific ordering)
    Performs data preprocessing which includes:
    - One hot encoding
    - Scaling
    Returns a single row dataframe with all features for prediction
    '''
    # Create a single row dataframe from the json object
    df = pd.DataFrame(json_data,index=[0])

    # Extract all numeric values
    numeric = df.select_dtypes(include=['number']).columns.tolist()

    # Scale numeric values
    scaler = StandardScaler()
    df_scaled = df.copy()
    scaler.fit(main_df[numeric])
    df_scaled[numeric] = scaler.transform(df_scaled[numeric])
    
    # One hot encode categorical values
    categorical = df.select_dtypes(exclude=['number']).columns.tolist()

    # one hot encode categorical values
    ohe = OneHotEncoder(sparse=False,handle_unknown='ignore',drop='first')
    ohe.fit(main_df[categorical])

    df_ohe = pd.DataFrame(ohe.transform(df[categorical]),columns=ohe.get_feature_names_out(categorical))
    # Concatenate the scaled numeric and one hot encoded categorical values
    df_final = pd.concat([df_scaled[numeric],df_ohe],axis=1)
    
    # Return the final dataframe and original dataframe
    return df_final, df