from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "123"
db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column (db.String(50), nullable=False)
    post_code = db.Column (db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)

class OwnerForm(FlaskForm):
     first_name = StringField("Enter Owner's First Name")
     last_name = StringField("Enter Owner's Last Name")
     age = IntegerField("Enter Owner's Age")
     address = StringField("Enter Owner's Address")
     post_code = StringField("Enter Owner's Postcode")
     submit = SubmitField("Add")

@app.route("/")
def index():
    all_owners = Owner.query.all()
    return render_template("index.html", all_owners=all_owners)

@app.route("/add", methods=["GET","POST"])
def add():
    form = OwnerForm()
    if form.validate_on_submit():
        new_owner = Owner(first_name=form.first_name.data, last_name=form.last_name.data, age=form.age.data, address=form.address.data, post_code=form.post_code.data.upper())
        db.session.add(new_owner)
        db.session.commit()
        x = f'the name you added was {new_owner.first_name} {new_owner.last_name}, the age is {new_owner.age}, the address is {new_owner.address}, the post code is {new_owner.post_code}'
        return x
    return render_template ("add.html", form=form)

@app.route("/complete/<int:owner_id>")
def complete(owner_id):
    owner = Owner.query.get(owner_id)
    owner.complete = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/incomplete/<int:owner_id>")
def Incomplete(owner_id):
    owner = Owner.query.get(owner_id)
    owner.complete = False
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:owner_id>")
def delete(owner_id):
    owner = Owner.query.get(owner_id)
    db.session.delete(owner)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')