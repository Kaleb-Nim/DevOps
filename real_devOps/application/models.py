from application import db
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Float)
    sex = db.Column(db.String(10))
    bmi = db.Column(db.Float)
    children = db.Column(db.Float)
    smoker = db.Column(db.String(10))
    region = db.Column(db.String(10))
    prediction = db.Column(db.Float)
    predicted_on_date = db.Column(db.DateTime, nullable=False)