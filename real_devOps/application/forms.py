from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms.validators import (InputRequired, Length, NumberRange,
                                ValidationError)

class PredctionFormInsurance(FlaskForm):
    age = FloatField(
        "Age", validators=[InputRequired(), NumberRange(0, 10)]
    )
    bmi = FloatField(
        "BMI", validators=[InputRequired(), NumberRange(0, 10)]
    )
    children = FloatField(
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

class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = StringField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Login")
    