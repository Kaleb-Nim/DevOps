from application import db
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

sex_class_list = ['male','female']
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    smoker = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(10), nullable=False)
    prediction = db.Column(db.Float)
    predicted_on_date = db.Column(db.DateTime)

    # === Validation ===>
    # dtype
    # valid values (ie postive/negative)
    # range (if any)
    # length of string (if any)

    @validates("age")
    def validate_age(self,_,age):
        if type(age) is not int:
            raise AssertionError("Age must be a float")
        if age <= 0:
            raise AssertionError("Age must be positive")
        return age
    
    
    @validates("prediction")
    def validate_prediction(self,_,prediction):
        if type(prediction) is not float:
            raise AssertionError("Prediction must be a float")
        if prediction <= 0:
            raise AssertionError("Prediction must be positive")
        return prediction
    
# Create class to store images in database
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_file_path = db.Column(db.String, nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    image_type = db.Column(db.String(100), nullable=False)
    image_size = db.Column(db.Integer, nullable=False)
    uploaded_on_date = db.Column(db.DateTime)

    # === Validation ===>
    # dtype
    # valid values (ie postive/negative)
    # range (if any)
    # length of string (if any)

    @validates("image_name")
    def validate_image_name(self,_,image_name):
        if type(image_name) is not str:
            raise AssertionError("Image name must be a string")
        if len(image_name) <= 0:
            raise AssertionError("Image name must be a string")
        return image_name

    @validates("image_type")
    def validate_image_type(self,_,image_type):
        if type(image_type) is not str:
            raise AssertionError("Image type must be a string")
        if len(image_type) <= 0:
            raise AssertionError("Image type must be a string")
        return image_type

    @validates("image_size")
    def validate_image_size(self,_,image_size):
        if type(image_size) is not int:
            raise AssertionError("Image size must be an integer")
        if image_size <= 0:
            raise AssertionError("Image size must be positive")
        return image_size   