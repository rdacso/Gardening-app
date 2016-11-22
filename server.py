"""Gardening"""

from jinja2 import StrictUndefined

from datetime import datetime
from flask import Flask, jsonify,render_template, redirect, request, flash, session, json, url_for
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension

from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db

from helper import load_all_plant_types, load_all_alerts_types

UPLOAD_FOLDER = '../static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Homepage."""
    
    #display homepage
    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def confirm():
    """Log In."""

    #get the form variables
    email = request.form["email"]
    password = request.form["password"]

    #query User table to see if new user is actually an existing user
    user = User.query.filter_by(email=email).first()

    #conditional to check to see if the user exists. 
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/register', methods=['GET'])
def user_signin():
    """User sign in form."""

    #display registration form
    return render_template('user_form.html')

@app.route('/register',methods=['POST'])
def register_process():
    """User sign in form."""

    # Get form variables from registration form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    password = request.form["password"].encode('utf-8')

    #query User table to see if new user is actually an existing user
    new_user = User.query.filter_by(email=email).first()

    #conditional to check if user exists in db. If user exists, redirect to login. Otherwise add to db and redirect to user's profile page.
    if new_user:
        flash('You already exist! Please log in.')
        return redirect('/login')
    else: 
        new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
        
    #add new user to the database
        db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    session["user_id"] = new_user.user_id
    return redirect("/users/%s" % new_user.user_id)


@app.route('/users/<int:user_id>')
def user_info(user_id):
    """shows user info"""

    #show user information based off user_id
    user = User.query.get(user_id)

    #display all plant types
    load_plants = load_all_plant_types()

    #display all alert types
    load_alerts = load_all_alerts_types()

    return render_template("user_info.html", user=user, load_plants=load_plants, load_alerts=load_alerts)


@app.route('/addplants', methods=['POST'])
def add_plants():
    """User can add plants to their profiles """

    #get form variables
    plant_id = request.form['plant_id']
    #get user session id
    user_id = session.get('user_id')

    #conditional to verify user is logged in before plants are added.
    if user_id:
        user_plant = UserPlant.query.filter_by(user_id=user_id, plant_id=plant_id).first()

    else:
        raise Exception("No user logged in.")  
    
    #conditional that searches userplant table for existing plants. if it already exists, plant is left alone. if plant does not exist, it's added to the table.
    if user_plant:
        flash('Plant already exists!')
    else: 
        user_plant = UserPlant(plant_id=plant_id, user_id=user_id)
        flash('New plant added')
        db.session.add(user_plant)

    db.session.commit()


    return redirect("/users/" + str(user_id))

@app.route('/addalerts', methods=['POST'])
def add_alerts():

    """Users can add alerts to the plants on their profiles. """

    #get form variables
    user_plant_id = request.form.get('user_plant_id')
    alert_type_id = request.form.get('alert_type_id')
    date = request.form['date']
    user_id = session.get('user_id')

    #conditional to verify user is logged in before alerts are added.

    if user_id:
        user_alert = Alert.query.filter_by(alert_type_id=alert_type_id, user_plant_id=user_plant_id, date=date ).all()

    else:
        raise Exception("No user logged in.")  

    #conditional that searches userplant table for existing plants. if it already exists, plant is left alone. if plant does not exist, it's added to the table.
    if user_alert:
        flash('Alert updated!')
    else: 
        user_alert = Alert(user_plant_id=user_plant_id, alert_type_id=alert_type_id, date=date)
        flash('New alert added')
        db.session.add(user_alert)

    db.session.commit()
    
    return redirect("/users/" + str(user_id))


@app.route('/addqty.json', methods=['POST'])
def add_qty():
    """User can add quantity to plant in garden """

    #get form variables
    qty = request.form.get('qty')
    user_plant_id = request.form.get('user_plant_id')
    user_id = session.get('user_id')

     #conditional to verify user is logged in before alerts are added. If they are logged in, quantity is updated.
    if user_id:
        plant_number = UserPlant.query.get(user_plant_id)
        plant_number.qty = qty

    else:
        raise Exception("No user logged in.")  


    flash('Quantity updated')
    db.session.commit()

    return jsonify({'user_plant_id':user_plant_id, 'qty':qty})

@app.route('/completealert.json', methods=['POST'])
def complete_alert():
    """Mark alert task as complete """

    #get form variables
    completion = bool(request.form.get('completion'))
    user_plant_id = request.form.get('user_plant_id')
    user_id = session.get('user_id')

     #conditional to verify user is logged in before alerts are added. If they are logged in, task completion is updated.
    if user_id:
        alert_completion = Alert.query.get(user_plant_id)
        alert_completion.completion = completion

    else:
        raise Exception("No user logged in.")  


    flash('Task status updated')
    # db.session.add(plant_number)
    db.session.commit()

    return jsonify({'completion':completion, 'user_plant_id':user_plant_id})

@app.route('/logout')
def logout():
    """Log out."""
    #delete the session user_id
    del session["user_id"]
    flash("Logged Out.")
    #return user ot the homepage
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(host='0.0.0.0', port=5000)