from application import db
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash


sex_class_list = ['male','female']
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Float)
    sex = db.Column(db.String(10))
    bmi = db.Column(db.Float)
    children = db.Column(db.Float)
    smoker = db.Column(db.String(10))
    region = db.Column(db.String(10))
    prediction = db.Column(db.Float)
    predicted_on_date = db.Column(db.DateTime)
    # === Validation ===>
    # dtype
    # valid values (ie postive/negative)
    # range (if any)
    # length of string (if any)

    @validates("age")
    def validate_age(self,_,age):
        if type(age) is not float:
            raise AssertionError("Age must be a float")
        if age <= 0:
            raise AssertionError("Age must be positive")
        return age
    
    @validates("bmi")
    def validate_bmi(self,_,bmi):
        if type(bmi) is not float:
            raise AssertionError("BMI must be a float")
        if bmi <= 0:
            raise AssertionError("BMI must be positive")
        return bmi
    
    @validates("prediction")
    def validate_prediction(self,_,prediction):
        if type(prediction) is not float:
            raise AssertionError("Prediction must be a float")
        if prediction <= 0:
            raise AssertionError("Prediction must be positive")
        return prediction
    
