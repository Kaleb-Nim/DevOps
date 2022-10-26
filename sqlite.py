import sqlite3
json_prediction = {
    "age": 1,
    "bmi": 0.4,
    "children": 0.6,
    "sex_male":0,
    "smoker_yes":1,
    "region_northwest":1,
    "region_southeast":0,
    "region_southwest":0
}

class InsuranceDB:
    def __init__(self):
        self.con = sqlite3.connect("insurance.db")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        # self.cur.execute("""DROP TABLE IF EXISTS insurance""")
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS insurance (
            age float,
            bmi float,
            children float,
            sex_male boolean,
            smoker_yes boolean,
            region_northwest boolean,
            region_southeast boolean,
            region_southwest boolean 
            )
            """
        )
    def insert(self,item):
        self.cur.execute(
            """INSERT OR IGNORE INTO insurance VALUES (?,?,?,?,?,?,?,?)""" ,item
            )
        self.con.commit()
    
    def read_all(self):
        self.cur.execute("""SELECT * FROM insurance""")
        rows = self.cur.fetchall()
        return rows
