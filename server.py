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
    scheduled_alerts = Alert.query.all()
    user_weekly_plants = UserPlant.query.all()
    return render_template("user_info.html", user=user, load_plants=load_plants, load_alerts=load_alerts, scheduled_alerts=scheduled_alerts, user_weekly_plants=user_weekly_plants)


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
        user_plant.plant_id == plant_id
        flash('Plant already exists!')
    else: 
        user_plant = UserPlant(plant_id=plant_id, user_id=user_id)
        flash('New plant added')
        db.session.add(user_plant)

    db.session.commit()


    return redirect("/users/" + str(user_id))

@app.route('/addalerts', methods=['POST'])
def add_alerts():
    print "**********************", request.form['alert_type_id']

    user_plant_id = request.form.get('user_plant_id')
    alert_type_id = request.form.get('alert_type_id')
    date = request.form['date']
    user_id = session.get('user_id')
    print user_id, "******************************"


    user_alert = Alert.query.filter_by(alert_type_id=alert_type_id, user_plant_id=user_plant_id, date=date ).all()
    
    #conditional that searches userplant table for existing plants. if it already exists, plant is left alone. if plant does not exist, it's added to the table.
    if user_alert:
        # user_alert.date = date
        flash('Alert updated!')
    else: 
        user_alert = Alert(user_plant_id=user_plant_id, alert_type_id=alert_type_id, date=date)
        flash('New alert added')
        db.session.add(user_alert)

    db.session.commit()
    

    return redirect("/users/" + str(user_id))

@app.route('/alerts')
def alert_display():

    user_id = session.get('user_id')

    return redirect("/users/" + str(user_id))

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0', port=5000)