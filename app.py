from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm, EditPetForm

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
toolbar = DebugToolbarExtension(app)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
# db.create_all()

@app.route('/')
def show_home():
    """
    Renders the home page of the application.

    This function is a route handler for the root URL ("/"). It retrieves all the pets from the database using the
    `Pet.query.all()` method and passes them to the `home.html` template for rendering. The retrieved pets are passed
    as the `pets` variable to the template.

    Returns:
        The rendered `home.html` template with the `pets` variable passed to it.

    """
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def show_add_pet():
    """
    Route for adding a new pet to the database.

    This function handles both GET and POST requests to the '/add' endpoint. It renders the 'add_pet.html' template
    with a PetForm instance when the request method is GET. When the request method is POST, it validates the form data
    and creates a new Pet object with the form data. The new pet is then added to the database session and committed.
    Finally, the function redirects the user to the root URL ('/').

    Parameters:
        None

    Returns:
        - If the request method is GET, it renders the 'add_pet.html' template with the PetForm instance.
        - If the request method is POST and the form data is valid, it redirects the user to the root URL ('/').
        - If the request method is POST and the form data is invalid, it renders the 'add_pet.html' template with the
          PetForm instance and error messages.
    """
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes
        )
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    return render_template('add_pet.html', form=form)

@app.route('/<pet_id>', methods=['GET', 'POST'])
def show_edit_pet(pet_id):
    """
    Show a specific pet by its ID.

    This function handles both GET and POST requests to the '/<pet_id>' endpoint. It retrieves a pet object from the
    database based on the provided pet_id. It then creates an EditPetForm instance with the pet object as the form
    object. If the form is submitted and validated, it updates the pet object with the new form data and commits the
    changes to the database. Finally, it redirects the user back to the pet's detail page.

    Parameters:
        pet_id (int): The ID of the pet to be shown.

    Returns:
        - If the request method is GET, it renders the 'show_pet.html' template with the pet object and the EditPetForm
          instance.
        - If the request method is POST and the form data is valid, it redirects the user back to the pet's detail page.
        - If the request method is POST and the form data is invalid, it renders the 'show_pet.html' template with the
          pet object and the EditPetForm instance, along with error messages.
    """
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        pet.photo_url = photo_url
        pet.age = age
        pet.notes = notes
        db.session.add(pet)
        db.session.commit()
        return redirect(f'/{pet_id}')
    return render_template('show_pet.html', pet=pet, form=form)
