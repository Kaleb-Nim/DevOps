from flask_tailwind.sqlite import InsuranceDB

db = InsuranceDB()

# Testing data
preduction = {
    "age": 1,
    "bmi": 0.4,
    "children": 0.6,
    "sex":"female",
    "smoker":"no",
    "region": "southeast"
}

# Inserting data into database
db.insert(prediction)

# Reading data from database

for item in db.read_all():
    print(item)