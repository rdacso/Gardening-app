"""Gardening"""

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
    session["user_id"] = new_user.user_id
    return redirect("/users/%s" % new_user.user_id)

@app.route('/login', methods=['GET'])
def login():
    """Log In."""

    

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
    load_alerts = AlertType.query.all()
    return render_template("user_info.html", user=user, load_plants=load_plants, load_alerts=load_alerts)


@app.route('/addplants', methods=['POST'])
def add_plants():

    #get form variables
    plant_id = request.form['plant_id']
    #get user session id
    user_id = session.get('user_id')

    #check to see if user is logged in.
    if not user_id:
        raise Exception("No user logged in.")

    # query the userplant table for a specific plant id
    user_plant = UserPlant.query.filter_by(user_id=user_id, plant_id=plant_id).first()
    
    #conditional that searches userplant table for existing plants. if it already exists, plant is left alone. if plant does not exist, it's added to the table.
    if user_plant:
        user_plant.plant_id = plant_id
        flash('Plant updated!')
    else: 
        user_plant = UserPlant(plant_id=plant_id)
        user_plant.user_id = user_id
        flash('New plant added')
        db.session.add(user_plant)

    db.session.commit()


    return redirect("/users/" + str(user_id))

@app.route('/addalerts', methods=['POST'])
def add_alerts():

    alert_type_id = request.form['alert_type_id']

    user_id = session.get('user_id')
 

 #    new_plant = PlantType(common_name=common_name, soil_type=soil_type, fertility_requirement=fertility_requirement, watering_frequency=watering_frequency, shade_tolerance=shade_tolerance)
 # +    user_plant = UserPlant(qty=qty)
 # +    user_plant.plant_type = new_plant
 # +    user_plant.user = (user=user, user_plant)
 # +    #create a user object from the session user id
 # +    db.session.add(new_plant)
 # +    db.session.add(user_plant)
 # +    db.session.commit()
    new_alert = AlertType(alert_type_id=alert_type_id)
    user_alert = Alert(new_alert)
    
    db.session.add(new_alert)
    db.session.add(user_alert)
    db.session.commit()


    # alert_info = AlertType(fertility_bool=fertility_bool, fertility_occurence=fertility_occurence, fertility_alert_date=fertility_alert_date, watering_bool=watering_bool, watering_occurrence=watering_occurrence, watering_alert_date=watering_alert_date, trimming_bool=trimming_bool, trimming_occurrence=trimming_occurrence, trimming_alert_date=trimming_alert_date)
    # user_alert = UserPlant(up_id=up_id)
    # user_alert.alerts = alert_info



    db.session.add(alert_info)
    db.session.add(user_alert)
    db.session.commit()



    # user_alert = AlertType.query.filter_by(fertility_bool=fertility_bool, fertility_occurence=fertility_occurence, fertility_alert_date=fertility_alert_date, watering_bool=watering_bool, watering_occurrence=watering_occurrence, watering_alert_date=watering_alert_date, trimming_bool=trimming_bool, trimming_occurrence=trimming_occurrence, trimming_alert_date=trimming_alert_date).first()
    # print user_alert
    #conditional that searches userplant table for existing alerts. if it already exists, plant is left alone. if alert does not exist, it's added to the table.
    if user_alert:
        user_alert.user_plant_id = user_plant_id
        flash('alert updated!')
    else: 
        user_alert = Alert(alert_type_id=alert_type_id)
        user_plant.user_id = user_id
        flash('New alert added')
        db.session.add(user_alert)

    db.session.commit()

    

    return redirect("/users/" + str(user_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0', port=5000)
