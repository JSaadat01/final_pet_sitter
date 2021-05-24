from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    all_owners = Owner.query.all()
    return render_template("index.html", all_owners=all_owners)

@app.route("/add")
def add():
    new_owner = Owner(first_name='john', last_name='isac')
    db.session.add(new_owner)
    db.session.commit()
    x = f'the name you added was {new_owner.first_name} {new_owner.last_name}'
    return x

@app.route("/complete/<int:owner_id>")
def complete(owner_id):
    owner = Owner.query.get(owner_id)
    owner.complete = True
    db.session.commit()
    return "completed added owner"

@app.route("/incomplete/<int:owner_id>")
def Incomplete(owner_id):
    owner = Owner.query.get(owner_id)
    owner.complete = False
    db.session.commit()
    return "Incompleted added owner"


@app.route("/delete/<int:owner_id>")
def delete(owner_id):
    owner = Owner.query.get(owner_id)
    db.session.delete(owner)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')