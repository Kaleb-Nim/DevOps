from sqlite import InsuranceDB

db = InsuranceDB()

# Testing data

prediction = (
    0.1,
    0.4,
    0.6,
    0,
    1,
    1,
    0,
    0
)

# Inserting data into database
db.insert(prediction)

# Reading data from database

for item in db.read_all():
    print(item)