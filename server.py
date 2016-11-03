"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify,render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""
    #show homepage.html template
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    #query and display all users in database
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register')
def user_signin():
    """User sign in form."""
    
    return render_template('user_form.html')

@app.route('/register',methods=['POST'])
def register_process():
    """User sign in form."""


    # Get form variables
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    city = request.form["city"]
    state = request.form["state"]
    zip_code = request.form["zip_code"]
    alerts = request.form["alerts"]
    password = request.form["password"]


    new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, city=city, state=state, zip_code=zip_code, alerts=alerts, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash("You have been added! Please log in.")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/login')
def login():
    """Log In."""

    
    flash("Logged In.")
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def confirm():
    """Log In."""

    email = request.form["email"]

    user = User.query.filter_by(email=email).one()

    session["user_id"] = user.user_id
    flash("Logged In.")
    return redirect("/users/" + str(user.user_id))


@app.route('/users/<user_id>')
def user_info(user_id):
    """shows user info"""

    user = User.query.filter_by(user_id=user_id).one()



    return render_template("user_info.html", user=user)


@app.route('/addplants', methods=['POST'])
def add_plants():
    common_name= request.form["common_name"]
    soil_type = request.form["soil_type"]
    fertility_requirement = request.form["fertility_requirement"]
    watering_frequency = request.form["watering_frequency"]
    shade_tolerance = request.form["shade_tolerance"]

    new_plant = PlantType(common_name=common_name, soil_type=soil_type, fertility_requirement=fertility_requirement, watering_frequency=watering_frequency, shade_tolerance=shade_tolerance)
    user_plant = UserPlant(qty=qty)
    user_plant.plant_type = new_plant
    user_plant.user = (user=user, user_plant)
    #create a user object from the session user id
    db.session.add(new_plant)
    db.session.add(user_plant)
    db.session.commit()

    flash("Your new plant has been added!")
    return redirect("/users/<user_id>", user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0', port=5000)
