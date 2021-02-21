from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db
from flask import jsonify, request, Flask


# app = Flask(__name__)
# connect_to_db(app)

# Get all records from a table
#######################################

def load_all_alerts_types():
    """returns alert types available in db """
    load_alerts = AlertType.query.all()

    return load_alerts

def load_all_plant_types():
    """returns all plant types available in db """
    load_plants = PlantType.query.order_by(PlantType.common_name).all()
    
    return load_plants

# Query for specific records in database
#########################################
def search_user_plants(plant_id, user_id):
    """Query db for user's plants """
    user_plant= UserPlant.query.filter_by(plant_id=plant_id, user_id=user_id).all()

    return user_plant

def search_user_alerts(user_plant_id):
    """Query db for alerts specific to user's plants """
    
    user_alert= Alert.query.get(user_plant_id)

    return user_alert

def find_existing_user(email):
    """Query db for existing users """

    user = User.query.filter_by(email=email).first()

    return user


# add records to the database
#########################################
def add_new_user(first_name, last_name, email, phone_number, password):
    """Add new user to database. """

    new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
        
    #add new user to the database
    db.session.add(new_user)
    db.session.commit()

    return new_user

def add_new_plant(user_id, plant_id):
    """Add plant to database. """
        
    user_plant = UserPlant(plant_id=plant_id, user_id=user_id)
    db.session.add(user_plant)

    db.session.commit()

    return user_plant

def add_new_alert(user_plant_id, alert_type_id, date):
    """Add alert to database. """
    user_alert = Alert(user_plant_id=user_plant_id, alert_type_id=alert_type_id, date=date)
    db.session.add(user_alert)
    db.session.commit()

    return user_alert