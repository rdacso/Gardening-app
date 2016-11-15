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
    alert_id = db.Column(db.Integer, unique=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    qty = db.Column(db.Integer)

    # define relationship to garden
    plant_type = db.relationship("PlantType",
                            backref=db.backref("userplants"))
    user = db.relationship("User",

                           backref=db.backref("userplants"))

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
    temperateure_min = db.Column(db.Integer)



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
    completion = db.Column(db.Boolean)
    alert_type_id = db.Column(db.Integer, db.ForeignKey('alerttype.alert_type_id'))


    alert = db.relationship('UserPlant', backref=db.backref('alerts'))
    alert_type = db.relationship('AlertType', backref=db.backref('alerts'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Alert alert_id=%s user_plant_id=%s date=%s completion=%s alert_type_id=%s>" % (self.alert_id, self.user_plant_id, self.date, self.completion, self.alert_type_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gardening'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
