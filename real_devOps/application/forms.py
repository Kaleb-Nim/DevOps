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
