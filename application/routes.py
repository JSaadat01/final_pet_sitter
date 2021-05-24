from application import app, db
from flask import render_template, url_for, redirect, request
from application.forms import OwnerForm, PetForm
from application.models import Owner, Pet


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
        new_owner = Owner(
            first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            age=form.age.data, 
            address=form.address.data, 
            post_code=form.post_code.data.upper()
        )
        
        db.session.add(new_owner)  
        db.session.flush()     # This will allow me to access new user's id without querying it from database
        
        new_pet = Pet(
            name=form2.name.data, 
            age2=form2.age2.data, 
            colour=form2.colour.data, 
            address=form2.address.data, 
            breed=form2.breed.data, 
            type=form2.type.data, 
            post_code=form2.post_code.data,
            owner_id=new_owner.id        # Saving owner id
        )
        
        db.session.add(new_pet)
        db.session.commit()
                
        return redirect(url_for('index'))
    
    return render_template ("add.html", form=form, form2=form2)


@app.route("/add-pet/<int:owner_id>", methods=["GET","POST"])
def add_pet(owner_id):
    # Adding new pet for an owner
    form = PetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data, 
            age2=form.age2.data, 
            colour=form.colour.data, 
            address=form.address.data, 
            breed=form.breed.data, 
            type=form.type.data, 
            post_code=form.post_code.data,
            owner_id=owner_id
        )
        
        db.session.add(new_pet)
        db.session.commit()
        
        return redirect(url_for('index'))
        
    return render_template("add_pet.html", form=form)


@app.route("/delete/<int:owner_id>")
def delete(owner_id):
    owner = Owner.query.get(owner_id)
    pets = Pet.query.filter_by(owner_id=owner_id).all()
    # First deleting the pets one by one linked to an owner then deleting the owner
    # If we will delete the owner first it will throw an error
    for pet in pets:
        db.session.delete(pet)
    db.session.delete(owner)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:owner_id>", methods=["GET", "POST"])
def update(owner_id):
    
    form = OwnerForm()
    
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
    
    return render_template ("update.html", form=form)


@app.route("/update-pet/<int:pet_id>", methods=["GET", "POST"])
def update_pet(pet_id):
    # Same as update user
    form = PetForm()
    
    pet_to_be_updated = Pet.query.get(pet_id)
    
    if form.validate_on_submit():
        
        pet_to_be_updated.name = form.name.data
        pet_to_be_updated.age2 = form.age2.data
        pet_to_be_updated.address = form.address.data
        pet_to_be_updated.colour = form.colour.data
        pet_to_be_updated.type = form.type.data
        pet_to_be_updated.post_code = form.post_code.data
        pet_to_be_updated.breed = form.breed.data
        
        db.session.commit()
        
        return redirect(url_for("index"))
    
    elif request.method == "GET": # Automatically fills in forms with data (making it easier if there is a typo)
        
        form.name.data = pet_to_be_updated.name
        form.age2.data = pet_to_be_updated.age2 
        form.address.data = pet_to_be_updated.address
        form.colour.data = pet_to_be_updated.colour
        form.type.data = pet_to_be_updated.type
        form.post_code.data = pet_to_be_updated.post_code
        form.breed.data = pet_to_be_updated.breed

    return render_template ("update_pet.html", form=form)
