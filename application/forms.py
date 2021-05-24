from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


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
