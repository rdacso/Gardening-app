"""Movie Ratings."""

from jinja2 import StrictUndefined

from datetime import datetime
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


@app.route('/register', methods=['GET'])
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

    #assign form variables to new_user variable
    new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, city=city, state=state, zip_code=zip_code, alerts=alerts, password=password)
    #add new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)

@app.route('/login', methods=['GET'])
def login():
    """Log In."""

    
    flash("Logged In.")
    #show the login template
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def confirm():
    """Log In."""
    #get the form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""
    #delete the session user_id
    del session["user_id"]
    flash("Logged Out.")
    #return user ot the homepage
    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    #query and display all users in database
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """shows user info"""
    #show user information based off user_id
    user = User.query.get(user_id)
    load_plants = PlantType.query.all()
    return render_template("user_info.html", user=user, load_plants=load_plants)


@app.route('/addplants', methods=['POST'])
def add_plants():

    #get form variables
    # common_name= request.form["common_name"]
    # fertility_requirement = request.form["fertility_requirement"]
    # # watering_frequency = datetime.now()
    # shade_tolerance = request.form["shade_tolerance"]
    # qty = request.form['qty']

    print 'I got here ****'

    plant_id = request.form['plant_id']
    user_id = session.get('user_id')

    #
    user_plant = UserPlant(plant_id=plant_id)
    # user_plant.plant_type = new_plant
    user_plant.user_id = user_id
    # db.session.add(new_plant)
    db.session.add(user_plant)

    db.session.commit()


    flash("Your new plant has been added!")

    # score = int(request.form["score"])

    # user_id = session.get("user_id")
    # if not user_id:
    #     raise Exception("No user logged in.")

    # rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    # if rating:
    #     rating.score = score
    #     flash("Rating updated.")

    # else:
    #     rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
    #     flash("Rating added.")
    #     db.session.add(rating)

    # db.session.commit()

    # return redirect("/movies/%s" % movie_id)
    return redirect("/users/" + str(user_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0', port=5000)
