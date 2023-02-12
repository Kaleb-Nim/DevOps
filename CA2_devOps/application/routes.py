from application import app
from flask import render_template, jsonify, request, redirect, url_for, flash
from application.forms import PredctionFormInsurance, LoginForm
from flask import render_template, request, flash
from application import ai_model
from application import db
from application.models import Entry
from datetime import datetime
from application.utilities import preProcess


def get_entries_sorted(sort="latest"):
    print("==>> sort: ", sort)
    try:
        if sort == "oldest":
            # sort by asc predicted_on_date
            entries = db.session.execute(
                db.select(Entry).order_by(Entry.predicted_on_date.asc())
            ).scalars()
        elif sort == "highestCost":
            # sort by desc prediction
            entries = db.session.execute(
                db.select(Entry).order_by(Entry.prediction.desc())
            ).scalars()
        elif sort == "lowestCost":
            # sort by asc prediction
            entries = db.session.execute(
                db.select(Entry).order_by(Entry.prediction.asc())
            ).scalars()
        else:

            # sort by desc predicted_on_date
            print("==> going thru default")
            entries = db.session.execute(
                db.select(Entry).order_by(Entry.predicted_on_date.desc())
            ).scalars()
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


# Function to delete an entry
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


# Function to add new prediction
def add_to_db(new_pred):
    try:
        db.session.add(new_pred)
        db.session.commit()
        return new_pred.id
    except Exception as error:
        db.session.rollback()
        print(error, "danger")
        return None


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
        "predicted_on_date": entry.predicted_on_date,
    }
    # Convert the data to json
    result = jsonify(data)
    return result  # response back
    # Handles http://127.0.0.1:5000/hello

# API add entry to db
@app.route("/api/add", methods=["POST"])
def api_add():
    # retrieve the entry using id from client
    data = request.get_json()
    print("==>> data: ", data)
    # Prepare a dictionary for json conversion
    new_entry = Entry(
                age=data.age,
                sex=data.sex,
                bmi=data.bmi,
                children=data.children,
                smoker=data.smoker,
                region=data.region,
                prediction=prediction,
                predicted_on_date=datetime.now(),
    )
    # Add the new entry to db
    id = add_to_db(new_entry)
    return 

# Handles http://127.0.0.1:5000/
@app.route("/")
@app.route("/index")
def index_page():
    return render_template("login.html", title="Kaleb Health insurance prediction")


# Home Page
@app.route("/home")
def home_page():
    return render_template("index.html", title="Home Page for Health Cost prediction")


# Handles http://127.0.0.1:5000/form
@app.route("/forms", methods=["GET"])
def form_page():
    form1 = PredctionFormInsurance()
    return render_template(
        "forms.html", form=form1, title="Kaleb Health insurance prediction"
    )


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
            # if age or bmi or children is negative, return 400 
            if age < 0 or bmi < 0 or children < 0:
                print("==>> age or bmi or children is negative")
                return "Invalid data entry", 400 

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
            prediction = float("{0:.2f}".format(ai_model.predict(prediction_input)[0]))
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
            return render_template(
                "forms.html", form=form, title="Kaleb Health insurance prediction", predictedCost=prediction
            )

        else:
            print("==>> form.validate_on_submit() is False")
            flash("Error, cannot proceed with prediction", "danger")
    return render_template(
        "forms.html", form=form, title="Kaleb Health insurance prediction"
    )


# Handles http://127.0.0.1:5000/predictions_history
# Handles GET request of different sortings of the history using query parameters
@app.route("/history", methods=["GET"])
def predictions_history():
    sort_by = request.args.get("sort", "latest")
    print("==>> predictions_history() called")
    entries = get_entries_sorted(sort_by)
    print("==>> entries: ", entries)
    return render_template(
        "history.html",
        entries=entries,
        title="Prediction History",
    )


# Handles http://127.0.01.5000/api/delete
@app.route("/remove", methods=["POST"])
def remove():
    sort_by = request.args.get("sort", "latest")
    form = Entry()
    req = request.form
    id = req["id"]
    remove_entry(id)
    return render_template(
        "history.html",
        title="Prediction History",
        form=form,
        entries=get_entries_sorted(sort_by),
    )


# Handles Login verifycation
@app.route("/login", methods=["post"])
def verifyLogin():
    login_form = LoginForm()
    print("==>> verifyLogin() called")
    vaild_credentials = {
        "kaleb.nim@gmail.com": "123",
        "sohhongyu@gmail.com": "123",
    }
    print(f"==> login_form: {request.form}")
    
    try:
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip().lower()
    except Exception as error:
        print("==>> request.form error: ", error)


    if email in vaild_credentials and password == vaild_credentials[email]:
        print("==>> Login success")
        return render_template(
            "login.html", title="Login", login_success=True, form=login_form
        )
    else:
        print("==>> Login failed")
        return render_template(
            "login.html", title="Login", login_success="print_error", form=login_form
        )


# 404 error handler, handles all 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="404"), 404
