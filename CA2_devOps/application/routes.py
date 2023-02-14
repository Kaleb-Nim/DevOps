from application import app
from flask import render_template, jsonify, request, redirect, url_for, flash
from application.forms import PredctionFormInsurance, LoginForm, PredctionImageForm
from flask import render_template, request, flash
from application import ai_model
from application import db
from application.models import Entry ,EntryCifar
from datetime import datetime
from application.utilities import load_img, reshape_image,make_prediction
from datetime import datetime as dt
from werkzeug.utils import secure_filename
import os

def get_entries_sorted(sort="latest"):
    print("==>> sort: ", sort)
    try:
        if sort == "oldest":
            # sort by asc predicted_on_date
            entries = db.session.execute(
                db.select(EntryCifar).order_by(EntryCifar.predicted_on_date.asc())
            ).scalars()
        elif sort == "highestConfidence":
            # sort by desc prediction
            entries = db.session.execute(
                db.select(EntryCifar).order_by(EntryCifar.prediction_prob.desc())
            ).scalars()
        elif sort == "lowestConfidence":
            # sort by asc prediction
            entries = db.session.execute(
                db.select(EntryCifar).order_by(EntryCifar.prediction_prob.asc())
            ).scalars()
        else:

            # sort by desc predicted_on_date
            print("==> going thru default")
            entries = db.session.execute(
                db.select(EntryCifar).order_by(EntryCifar.predicted_on_date.desc())
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
        result = db.get_or_404(EntryCifar, id)
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
        entry = EntryCifar.query.filter(EntryCifar.id == id).first()
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
        print(f'new_pred: {new_pred.prediction}')
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
    form1 = PredctionImageForm()
    return render_template(
        "forms.html", form=form1, title="Kaleb Health insurance prediction"
    )

# Handles http://127.0.0.1:500/predict
@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = PredctionImageForm()
    print("==>> predict() called")
    if request.method == "POST" and form.validate_on_submit():
        print("==>> form errors: ", form.errors)
        print("==>> WOI WOI WOI form.image: ", form.image.data)
        upload_time = dt.now().strftime("%Y%m%d%H%M%S%f")
        upload_time_db = datetime.now()
        # Get latest image from static/images folder
        # imgPath = get_latest_image() # to do - get the latest image
        base_path = os.path.dirname(__file__) + "\\static\\images"

        # Get the data from the POST request.
        dataset_type = form.dataset_type.data
        model_name = form.model_name.data
        file = form.image.data


        # Save the image to the static folder
        filename = secure_filename(file.filename)
        # Extract out the extension and filename
        file_name_ext = os.path.splitext(filename)
        full_filename = f'{file_name_ext[0]}_{upload_time}{file_name_ext[1]}'
        print("==>> full_filename: ", full_filename)

        image_to_predict_file_path = os.path.join(base_path, full_filename)
        file.save(image_to_predict_file_path)
        print(f'Image saved at: {image_to_predict_file_path}')

        # Load the image + data pre-processing ( Handled in utils.py )
        image_to_predict = load_img(f'{image_to_predict_file_path}')

        # Get the prediction
        try:
            prediction,prediction_prob = make_prediction(image_to_predict,model_name = model_name)
        except Exception as error:
            print("==>> Error: ", error)
            flash("Error: ", error)
            return redirect(url_for("form_page"))
        # Check all datatypes
        print("==>> type(image_to_predict_file_path): ", type(image_to_predict_file_path))
        print("==>> type(prediction): ", type(prediction))
        print("==>> type(prediction_prob): ", type(prediction_prob))
        print("==>> type(dataset_type): ", type(dataset_type))
        print("==>> type(model_name): ", type(model_name))
        print("==>> type(upload_time_db): ", type(upload_time_db))

        image_to_path_from_history_page = f'../static/images/{full_filename}'
        # Save the prediction to db
        new_entry = EntryCifar(
            image_path = image_to_path_from_history_page,
            prediction = prediction,
            prediction_prob = prediction_prob,
            dataset_type = dataset_type,
            model_name = model_name,
            predicted_on_date = upload_time_db
        )

        print("==>> new_entry: ", new_entry)
        id_added = add_to_db(new_entry)
        print("==>>Succesfull added id: ", id_added)
        return render_template(
            "forms.html", form=form, title="Kaleb Health insurance prediction", predictedCost=prediction,confidence = prediction_prob
        )
    else:
        print("==>> form.validate_on_submit() is False")
        print("==>> form.errors: ", form.errors)
    return redirect(url_for("form_page") )

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

# Handles GET request of different sortings of the history using query parameters
@app.route("/history_cifar", methods=["GET"])
def predictions_history_cifar():
    sort_by = request.args.get("sort", "latest")
    print("==>> predictions_history() called")
    entries = get_entries_sorted(sort_by)
    print("==>> entries: ", entries)
    return render_template(
        "history_cifar.html",
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
