from application import db


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    address = db.Column (db.String(50))
    post_code = db.Column (db.String(50))
    show = db.Column(db.Boolean, default=False)
    pets = db.relationship('Pet', backref='owner')       # NEW LINE ADDED HERE


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age2 = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    post_code = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)   # NEW LINE HERE
