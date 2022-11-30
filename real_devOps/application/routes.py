from application import app
from flask import render_template, jsonify, request, redirect, url_for, flash
from application.forms import PredctionFormInsurance, LoginForm
from flask import render_template, request, flash
from application import ai_model
from application import db
from application.models import Entry
from datetime import datetime
from application.utilities import preProcess


def get_entries():
    try:
        # entries = Entry.query.all() # version 2
        entries = db.session.execute(db.select(Entry).order_by(Entry.id)).scalars()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def get_entry(id):
    """
    function to get an entry by id
    """
    try:
        # entries = Entry.query.filter(Entry.id==id) version 2
        result = db.get_or_404(Entry, id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0
        
def remove_entry(id):
    """
    function to get an entry by id
    """
    try:
        entry = Entry.query.filter(Entry.id == id).first()
        db.session.delete(entry)
        db.session.commit()
        return 1
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

# API get entry
@app.route("/api/get/<id>", methods=["GET"])
def api_get(id):
    # retrieve the entry using id from client
    entry = get_entry(int(id))
    # Prepare a dictionary for json conversion
    data = {
        "id": entry.id,
        "age": entry.age,
        "sex": entry.sex,
        "bmi": entry.bmi,
        "children": entry.children,
        "smoker": entry.smoker,
        "region": entry.region,
        "prediction": entry.prediction,
        "predicted_on_date": entry.predicted_on_date
    }
    # Convert the data to json
    result = jsonify(data)
    return result  # response back
    # Handles http://127.0.0.1:5000/hello

#API delete entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id): 
    entry = remove_entry(int(id))
    return jsonify({'result':'ok'})



# Handles http://127.0.0.1:5000/
@app.route("/")
@app.route("/index")
def index_page():
    return render_template("index.html", title="Kaleb Health insurance prediction")


# Handles http://127.0.0.1:5000/form
@app.route("/forms", methods=["GET"])
def form_page():
    form1 = PredctionFormInsurance()
    return render_template(
        "forms.html", form=form1, title="Kaleb Health insurance prediction"
    )


# Handles https://127.0.0.1:5000/login
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", title="Login")


# Function to add new prediction or user
def add_to_db(new_pred):
    try:
        db.session.add(new_pred)
        db.session.commit()
        return new_pred.id
    except Exception as error:
        db.session.rollback()
        print(error, "danger")
        return None


# Handles http://127.0.0.1:500/predict
@app.route("/predict", methods=["GET", "POST"])
def predict():
    print("==>> predict() called")
    form = PredctionFormInsurance()
    print("==>> form: ", form)
    if request.method == "POST":
        if form.validate_on_submit():
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
                "age": age,
                "sex": sex,
                "bmi": bmi,
                "children": children,
                "smoker": smoker,
                "region": region,
            }
            # Preprocess the data
            try:
                prediction_input = preProcess(prediciton_format)
            except Exception as error:
                print("==>> preProcess() error: ", error)
            # Predict
            prediction = float(ai_model.predict(prediction_input)[0])
            print("==>> prediction: ", type(prediction))

            # print all parameters to the console
            print("==>> age: ", age)
            print("==>>sex", sex)
            print("==>>bmi", bmi)
            print("==>>children", children)
            print("==>>smoker", smoker)
            print("==>>region", region)
            print("==>>prediction", prediction)

            # Save the prediction to the database
            new_entry = Entry(
                age=age,
                sex=sex,
                bmi=bmi,
                children=children,
                smoker=smoker,
                region=region,
                prediction=prediction,
                predicted_on_date=datetime.now(),
            )
            print("==>> new_entry: ", new_entry)
            id_added = add_to_db(new_entry)
            print("==>>Succesfull added id: ", id_added)
            # flash(f"Prediction: money money {prediction[0]}","success")

        else:
            print("==>> form.validate_on_submit() is False")
            # flash("Error, cannot proceed with prediction", "danger")
    return render_template(
        "forms.html", form=form, title="Kaleb Health insurance prediction"
    )


# Handles http://127.0.0.1:5000/predictions_history
@app.route("/history", methods=["GET"])
def predictions_history():
    print("==>> predictions_history() called")
    entries = get_entries()
    print("==>> entries: ", entries)
    return render_template(
        "history.html",
        entries=entries,
        title="Prediction History",
    )
