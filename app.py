from flask import Flask, render_template, json, request,redirect, sessions
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contact.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Fname = db.Column(db.String(120), nullable=False)
    Lname = db.Column(db.String(120), nullable=False)
    Country = db.Column(db.String(120), nullable=False)
    Subject = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Rateus(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with open('config.json', 'r') as c:
    params = json.load(c)['params']

@app.route("/about")
def about():
    return render_template("about.html", param=params)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        countryname = request.form['country']
        Sub = request.form['subject']
        contact = Contact(Fname=firstname, Lname=lastname, Country=countryname, Subject=Sub)
        db.session.add(contact)
        db.session.commit()
    
    contacts = Contact.query.all()
    return render_template("Contact.html", param=params, con=contacts)

@app.route("/rate", methods=['GET', 'POST'])
def rate():
    if request.method == "POST":
        Name = request.form['names']
        rate = request.form['rate']
        rateus = Rateus(name=Name, rate=rate)
        db.session.add(rateus)
        db.session.commit()

    alltodo = Rateus.query.all()
    return render_template("Reteus.html", alls=alltodo, param=params)

@app.route("/help")
def help():
    return render_template("help.html", param=params)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['Title']
        desc = request.form['descr']
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template("index.html", all=alltodo, param=params)

@app.route("/delete/<int:sno>")
def delete(sno):
    mytodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(mytodo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['Title']
        desc = request.form['descr']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    alltodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", mytodo=alltodo, param=params)

if __name__ == "__main__":
    app.run(debug=True, port=8000)