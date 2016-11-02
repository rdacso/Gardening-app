"""Models and database functions for Gardening app project"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime


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
    phone_number = db.Column(db.Integer)
    city = db.Column(db.String(25))
    state = db.Column(db.String(25))
    zipcode = db.Column(db.String(15))
    tmz = db.Column(db.DateTime)
    alerts = db.Column(db.Boolean)


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
                           backref=db.backref("userplants"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserPlant user_plant_id=%s plant_id=%s user_id=%s qty=%s>" % (
            self.user_plant_id, self.plant_id, self.user_id, self.qty)


class PlantType(db.Model):
    """gardens per user"""

    __tablename__ = 'plants'

    plant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plant_name = db.Column(db.String)
    spacing = db.Column(db.Integer)
    soil_ph_min = db.Column(db.Integer)
    soil_ph_max = db.Column(db.Integer)
    watering_frequency = db.Column(db.DateTime)
    sun_preference = db.Column(db.String)
    coloring = db.Column(db.String)
    height = db.Column(db.Integer)
    hardiness_zone_min = db.Column(db.Integer)
    hardiness_zone_max = db.Column(db.Integer)

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

        return "<AlertType alert_type_id=%s alert_type=%s>" % (self.alert_type_id, self.alert_type)

class Alert(db.Model):
    """Alerts on gardening website."""

    __tablename__ = "alerts"

    alert_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('userplants.up_id'),  unique=True)
    date = db.Column(db.DateTime)
    completion = db.Column(db.Boolean)
    alert_type_id = db.Column(db.Integer, db.ForeignKey('alerttype.alert_type_id'))


    alerts = db.relationship('UserPlant', backref=db.backref('alerts'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Alert alert_id=%s user_plant_id=%s date=%s completion=%s alert_type_id=%s>" % (self.alert_id, self.user_plant_id, self.date, self.completion, self.alert_type_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gardening'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
