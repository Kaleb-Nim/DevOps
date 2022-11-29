from application import app
from flask import render_template
from application.forms import PredctionFormInsurance
from flask import render_template, request, flash
from application import ai_model
from application import db
from application.models import Entry
from datetime import datetime
from application.utilities import preProcess, formatPrediction

# Handles http://127.0.0.1:5000/hello
@app.route("/hello")
def hello_world():
    return "<h1>Hello World</h1>"


# Handles http://127.0.0.1:5000/
@app.route("/")
@app.route("/index")
def index_page():
    form1 = PredctionFormInsurance()
    return render_template(
        "index.html", form=form1, title="Kaleb Health insurance prediction"
    )

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")

# Handles http://127.0.0.1:500/predict
@app.route("/predict", methods=["GET", "POST"])
def predict():
    print("==>> predict() called")
    form = PredctionFormInsurance()
    print("==>> form: ", form)
    if request.method == "POST":
        if form:
            print("==>> form errors: ", form.errors)
            print("==>> form.validate_on_submit() is True")
            # Get the data from the POST request.
            age = form.age.data
            sex = form.sex.data
            bmi = form.bmi.data
            children = form.children.data
            smoker = form.smoker.data
            region = form.region.data
            # Format the data
            prediciton_format = {
                'age':age,
                'sex':sex,
                'bmi':bmi,
                'children':children,
                'smoker':smoker,
                'region':region,
            }
            # Preprocess the data
            try:
                prediction_input = preProcess(prediciton_format)
            except Exception as error:
                print("==>> preProcess() error: ", error)
            # Predict
            prediction = ai_model.predict(prediction_input)
            # Save the prediction
            new_entry = Entry(
                age=age,
                sex=sex,
                bmi=bmi,
                children=children,
                smoker=smoker,
                region=region,
                prediction=prediction[0],
                date=datetime.now(),
            )
            add_entry(new_entry)
            flash(f"Prediction: money money {prediction[0]}","success")

        else:
            print("==>> form.validate_on_submit() is False")
            flash("Error, cannot proceed with prediction", "danger")
    return render_template(
        "index.html", form=form, title="Kaleb Health insurance prediction"
    )

