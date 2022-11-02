from flask import Flask, render_template, request, redirect  # add
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add

from sqlite import InsuranceDB
from utilis import preProcess, format, model,df_raw
print("==>> type(df_raw): ", type(df_raw))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insurance.db'  # add
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # add

db = InsuranceDB()  # add
# add

@app.route("/login", methods=['GET',"POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(f"Email password: {email},{password}")
        return redirect('/')
    return render_template("login.html")  # add


@app.route("/predict", methods=['GET',"POST"])
def predict_from_form():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(f"Email password: {email},{password}")
        return redirect('/')
    return render_template("form.html")  # add

@app.route("/prediction", methods=['GET',"POST"])
def savePrediction():
    if request.method == "POST":
        print("Prediction went through")
        # Get the data from the POST request.
        age = int(request.form['age'])
        bmi = int(request.form['bmi'])
        children = int(request.form['children'])
        sex = request.form['sex']
        smoker = request.form['smoker']
        region = request.form['region']
        # Format the data
        prediction, history = format(age=age,sex=sex,bmi=bmi,children=children,smoker=smoker,region=region)

        print("==>> type(prediction): ", type(prediction))
        prediction_input = preProcess(prediction,main_df=df_raw)

        # Predict
        prediction = model.predict(prediction_input)
        output = prediction[0]
        # return prediction  # add
        db.insert(history)

        return render_template("result.html", prediction_results=output)  # add

    return render_template("form.html")
@app.route("/history", methods=['GET'])
def history():
    return db.read_all()

@app.route("/result", methods=['GET'])
def result():
    return render_template("result.html")

if __name__ == "__main__":
   app.run(debug=True)