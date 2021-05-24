from flask import Flask, url_for, redirect, render_template, request
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

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age2 = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    post_code = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)


class OwnerForm(FlaskForm):
     first_name = StringField("Enter Owner's First Name")
     last_name = StringField("Enter Owner's Last Name")
     age = IntegerField("Enter Owner's Age")
     address = StringField("Enter Owner's Address")
     post_code = StringField("Enter Owner's Postcode")
     submit = SubmitField("Add")
class PetForm(FlaskForm):
    name = StringField("Enter Pet's Name")
    age2 = IntegerField("Enter Pet's Age")
    colour = StringField("Enter Pet's Colour")
    address = StringField("Enter Pet's Registered Address")
    type = StringField("Enter Pet's Species")
    breed = StringField("Enter Pet's Breed")
    post_code = StringField("Enter Pet's Registered's Postcode")
    submit = SubmitField("Add")
    
@app.route("/")
def index():
    all_owners = Owner.query.all()
    all_pets = Pet.query.all()
    return render_template("index.html", all_owners=all_owners, all_pets=all_pets)

@app.route("/add", methods=["GET","POST"])
def add():
    form = OwnerForm()
    form2 = PetForm()
    if form.validate_on_submit():
        new_owner = Owner(first_name=form.first_name.data, last_name=form.last_name.data, age=form.age.data, address=form.address.data, post_code=form.post_code.data.upper())
        new_pet = Pet(name=form2.name.data, age2=form2.age2.data, colour=form2.colour.data, address=form2.address.data, breed=form2.breed.data, type=form2.type.data, post_code=form2.post_code.data)
        db.session.add(new_owner, new_pet)
        db.session.commit()
        y = f'The pet name you added was {new_pet.name}, the age of the pet is {new_pet.age2}, the colour of the pet is {new_pet.colour}, the registered address is {new_pet.address}, the registered post code is {new_pet.post_code.upper()}, the species is {new_pet.type} and the the breed is {new_pet.breed}'
        x = f'The name you added was {new_owner.first_name} {new_owner.last_name}, the age is {new_owner.age}, the address is {new_owner.address}, the post code is {new_owner.post_code}. | '
        return x+y
    return render_template ("add.html", form=form, form2=form2)

@app.route("/complete/<int:owner_id>")
def complete(owner_id):
    owner = Owner.query.get(owner_id)
    owner.complete = True
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/incomplete/<int:owner_id>")
def incomplete(owner_id):
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

@app.route("/update/<int:owner_id>", methods=["GET", "POST"])
def update(owner_id):
    form = OwnerForm()
    form2 = PetForm()
    owner_to_be_updated = Owner.query.get(owner_id)
    if form.validate_on_submit():
        owner_to_be_updated.first_name = form.first_name.data
        owner_to_be_updated.last_name = form.last_name.data
        owner_to_be_updated.age = form.age.data
        owner_to_be_updated.address = form.address.data
        owner_to_be_updated.post_code = form.post_code.data
        db.session.commit()
        return redirect(url_for("index"))
    elif request.method == "GET": # Automatically fills in forms with data (making it easier if there is a typo)
        form.first_name.data = owner_to_be_updated.first_name
        form.last_name.data = owner_to_be_updated.last_name 
        form.age.data = owner_to_be_updated.age
        form.address.data = owner_to_be_updated.address
        form.post_code.data = owner_to_be_updated.post_code
    return render_template ("update.html", form=form, form2=form2)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')








