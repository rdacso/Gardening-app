"""Models and database functions for Gardening app project"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime
from sqlalchemy_utils import PhoneNumber
import json




# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """Table to store users for gardening website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(65), nullable=True)
    last_name = db.Column(db.String(65))
    phone_number = db.Column(db.String)
    city = db.Column(db.String(25))
    state = db.Column(db.String(25))
    zip_code = db.Column(db.String(15))
    tmz = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    alerts = db.Column(db.Boolean, default=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class UserPlant(db.Model):
    """Plants added by individual users"""

    __tablename__ = "userplants"

    up_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    qty = db.Column(db.Integer)

    # define relationship to garden
    plant_type = db.relationship("PlantType",
                            backref=db.backref("userplants"))
    user = db.relationship("User",
                           backref=db.backref("userplants", 
                           order_by="UserPlant.plant_id"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserPlant up_id=%s plant_id=%s user_id=%s qty=%s>" % (self.up_id, self.plant_id, self.user_id, self.qty)


class PlantType(db.Model):
    """gardens per user"""

    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    common_name = db.Column(db.String)
    duration = db.Column(db.String)
    active_growth_period = db.Column(db.String)
    flower_color = db.Column(db.String)
    flower_conspicuous = db.Column(db.String)
    foliage_color = db.Column(db.String)
    height = db.Column(db.Float)
    adapted_to_coarse_textured_soil = db.Column(db.String)
    adapted_to_medium_textured_soil = db.Column(db.String)
    adapted_to_fine_textured_soil = db.Column(db.String)
    drought_tolerance = db.Column(db.String)
    fertility_requirement = db.Column(db.String)
    soil_ph_min = db.Column(db.Float)
    soil_ph_max = db.Column(db.Float)
    shade_tolerance = db.Column(db.String)
    temperature_min = db.Column(db.Integer)
    plant_image = db.Column(db.LargeBinary)



    # Define relationship to user


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Plants plant_id=%s plant_name=%s>" % (self.plant_id, self.plant_name)

  
class AlertType(db.Model):
    """gardens per user"""

    __tablename__ = 'alerttype'

    alert_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alert_type = db.Column(db.String)

    # Define relationship to user

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.alert_type)

class Alert(db.Model):
    """Alerts on gardening website."""

    __tablename__ = "alerts"

    alert_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('userplants.up_id'))
    date = db.Column(db.DateTime)
    completion = db.Column(db.Boolean, default='False')
    alert_type_id = db.Column(db.Integer, db.ForeignKey('alerttype.alert_type_id'))


    alert = db.relationship('UserPlant', backref=db.backref('alerts'))
    alert_type = db.relationship('AlertType', backref=db.backref('alerts'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Alert alert_id=%s user_plant_id=%s date=%s completion=%s alert_type_id=%s>" % (self.alert_id, self.user_plant_id, self.date, self.completion, self.alert_type_id)

def example_data():
    """Create some sample data for test database """

    # User.query.delete()
    # UserPlant.query.delete()
    # Alert.query.delete()

    #Two test users with different gardens.

    tester1 = User(first_name='Al', last_name='Beback', email='al@test.com', password='admin123')

    tester2 = User(first_name='Freida', last_name='Beemee', email='fb@test.com', password='admin456')

    #Three plants for the users to select from

    plant1 = PlantType(common_name='rose', duration='Perennial', active_growth_period='Spring', flower_color='White', flower_conspicuous='yes', foliage_color='green', height=3.0, adapted_to_coarse_textured_soil='no', adapted_to_medium_textured_soil='yes', adapted_to_fine_textured_soil='no', fertility_requirement='medium', soil_ph_min=6.0, soil_ph_max=8.0, shade_tolerance='intermediate', temperature_min=-38, plant_image='www.google.com')

    plant2 = PlantType(common_name='tulip', duration='Perennial', active_growth_period='Fall', flower_color='Blue', flower_conspicuous='no', foliage_color='green', height=3.0, adapted_to_coarse_textured_soil='yes', adapted_to_medium_textured_soil='yes', adapted_to_fine_textured_soil='no', fertility_requirement='low', soil_ph_min=6.0, soil_ph_max=1.0, shade_tolerance='intermediate', temperature_min=-38, plant_image='www.facebook.com')

    plant3 = PlantType(common_name='bluebell', duration='Perennial', active_growth_period='Winter', flower_color='Purple', flower_conspicuous='yes', foliage_color='silver', height=3.0, adapted_to_coarse_textured_soil='no', adapted_to_medium_textured_soil='yes', adapted_to_fine_textured_soil='yes', fertility_requirement='high', soil_ph_min=22.0, soil_ph_max=8.0, shade_tolerance='high', temperature_min=-38, plant_image='www.youtube.com')

    #Plants selected for user gardens

    tester1plant = UserPlant(plant_id=1, user_id=1, qty=14)

    tester2plant = UserPlant(plant_id=2, user_id=2, qty=500)

    #Three alerts for users to select from

    alerttype1 = AlertType(alert_type='watering')

    alerttype2 = AlertType(alert_type='trimming')

    alerttype3 = AlertType(alert_type='fertilizing')

    
    #Alerts selected for user's gardens.

    tester1alert = Alert(user_plant_id=1, date='2016-12-28 00:00:00', completion=False, alert_type_id=1)

    tester2alert = Alert(user_plant_id=2, date='2016-12-29 00:00:00', completion=False, alert_type_id=3)

    db.session.add_all([tester1, tester2, plant1, plant2, plant3, tester1plant, tester2plant, alerttype1, alerttype2, alerttype3, tester1alert, tester2alert])

    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///gardening'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = True

    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."