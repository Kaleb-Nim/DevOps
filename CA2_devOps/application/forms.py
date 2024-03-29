from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField,IntegerField
from wtforms.validators import (InputRequired, Length, NumberRange,
                                ValidationError)

from flask_wtf.file import FileField, FileAllowed, FileRequired

class PredctionFormInsurance(FlaskForm):
    age = IntegerField(
        "Age", validators=[InputRequired(), NumberRange(1, 120)]
    )
    bmi = FloatField(
        "BMI", validators=[InputRequired(), NumberRange(1, 50)]
    )
    children = IntegerField(
        "Children", validators=[InputRequired(), NumberRange(0, 10)]
    )
    smoker = SelectField(
        "Smoker", choices= [("yes", "Smoker"), ("no", "Non-Smoker")], validators=[InputRequired()]
    )
    sex = SelectField(
        u'sex', choices=[('male', 'M'), ('female', 'F')], validators=[InputRequired()]
    )
    region = SelectField(
        u'region', choices=[('southeast', 'southeast'), ('southwest', 'southwest'), ('northeast', 'northeast'), ('northwest', 'northwest')], validators=[InputRequired()]
    )
    submit = SubmitField("Predict")

# Form to store image upload data
class PredctionImageForm(FlaskForm):
    image = FileField(
        "Image", validators=[FileAllowed(["jpg", "png", "jpeg"]),InputRequired()]
    )
    model_name = SelectField(
        "Model Name", choices= [("vgg19", "VGG19"), ("Cifar100Efficient", "EfficientNet")], validators=[InputRequired()]
    )
    dataset_type = SelectField(
        "Dataset Type", choices= [("fine", "FINE"), ("corse", "CORSE")], validators=[InputRequired()]
    )
    submit = SubmitField("Predict Image!")

class LoginForm(FlaskForm):
    email_address = StringField(
        "Email Address", validators=[InputRequired(), Length(min=4, max=50)]
    )
    password = StringField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Login")

