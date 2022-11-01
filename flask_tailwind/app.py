from flask import Flask, render_template, request, redirect  # add
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add

from sqlite import InsuranceDB


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # add
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # add

db = InsuranceDB()  # add
# add

@app.route("/", methods=['GET'])
def home():
   if request.method == "POST": # add
       name = request.form['name']
       new_task = Task(name=name)
       db.session.add(new_task)
       db.session.commit()
       return redirect('/')
#    else:
#        tasks = Task.query.order_by(Task.created_at).all()  # add
   return render_template("home.html")  # add

@app.route("/login", methods=['GET'])
def login():
   return render_template("login.html")  # add

if __name__ == "__main__":
   app.run(debug=True)