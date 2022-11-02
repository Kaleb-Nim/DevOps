import sqlite3


class InsuranceDB:
    def __init__(self):
        self.con = sqlite3.connect("insurance.db",check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        # self.cur.execute("""DROP TABLE IF EXISTS insurance""")
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS insurance (
            age float,
            bmi float,
            children float,
            sex varchar(10),
            smoker varchar(10),
            region varchar(50) )
            """
        )
    def insert(self,item):
        print(item)
        self.cur.execute(
            """INSERT OR IGNORE INTO insurance VALUES (?,?,?,?,?,?)""" ,item
            )
        self.con.commit()
    
    def read_all(self):
        self.cur.execute("""SELECT * FROM insurance""")
        rows = self.cur.fetchall()
        return rows
