from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db
from flask import jsonify, request
import math

# Get all records from a table
#######################################

def load_all_alerts_types():
    """returns alert types available in db """
    load_alerts = AlertType.query.all()

    return load_alerts

def load_all_plant_types():
    """returns all plant types available in db """
    load_plants = PlantType.query.all()
    
    return load_plants

# add records to the database
#########################################
def add_plants(user_id, plant_id):
    """Search the userplant table for existing plants. If it exists, plant is left alone. If plant does not exist, it is added."""

    user_plant = UserPlant.query.filter_by(user_id=user_id, plant_id=plant_id).first()

    if user_plant:
        user_plant.plant_id == plant_id
        flash('Plant already exists!')
    else: 
        user_plant = UserPlant(plant_id=plant_id, user_id=user_id)
        flash('New plant added')
        db.session.add(user_plant)

    db.session.commit()

    return user_plant


def add_alerts(alert_type_id, user_plant_id, date):
    """Search the alert table for existing alert. If it exists, alert is left alone. If alert does not exist, it is added."""

    user_alert = Alert.query.filter_by(alert_type_id=alert_type_id, user_plant_id=user_plant_id, date=date ).all()

    if user_alert:
        flash('Alert already exists!')
    else: 
        user_alert = Alert(user_plant_id=user_plant_id, alert_type_id=alert_type_id, date=date)
        flash('New alert added')
        db.session.add(user_alert)

    db.session.commit()

    return user_alert

def add_users(first_name, last_name, email, phone_number, city, state, zip_code, password):
    """search the user table for existing user. If they exist, user is left alone. If user does not exist, they are added."""
    new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, city=city, state=state, zip_code=zip_code, password=password)

    if new_user:
        flash('User already exists! Please check your username or password and try again.')
    else: 
        new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, city=city, state=state, zip_code=zip_code, password=password)
        flash('New user added')
        db.session.add(new_user)

    db.session.commit()

    return new_user

def get_alert_type_names():
    alert_type_names = db.session.query(AlertType.alert_type, Alert.date).join(Alert).all()

    for alert_type, date in alert_type_names:
        print alert_type, date
