"""Utility file to seed plant database from USDA data/"""

from sqlalchemy import func
from model import User, UserPlant, PlantType, AlertType, Alert
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime



def load_plants():
    """Load users from u.user into database."""

    print "Plants"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    PlantType.query.delete()

    for i, row in enumerate(open('seed_data/plants.txt')):
        row = row.strip('"')
        row = row.rstrip()
        common_name, duration, active_growth_period, flower_color, flower_conspicuous, foliage_color, height, adapted_to_coarse_textured_soil, adapted_to_medium_textured_soil, adapted_to_fine_textured_soil, drought_tolerance, fertility_requirement, soil_ph_min, soil_ph_max, shade_tolerance, temperateure_min   = row.split('","')

        if common_name and duration and active_growth_period and flower_color and flower_conspicuous and foliage_color and height and adapted_to_coarse_textured_soil and adapted_to_medium_textured_soil and adapted_to_fine_textured_soil and drought_tolerance and fertility_requirement and soil_ph_min and soil_ph_max and shade_tolerance and temperateure_min:
            plant = PlantType(common_name=common_name,
                        duration=duration,
                        active_growth_period=active_growth_period,
                        flower_color=flower_color,
                        flower_conspicuous=flower_conspicuous,
                        foliage_color=foliage_color,
                        height=height,
                        adapted_to_coarse_textured_soil=adapted_to_coarse_textured_soil,
                        adapted_to_medium_textured_soil=adapted_to_medium_textured_soil,
                        adapted_to_fine_textured_soil=adapted_to_fine_textured_soil,
                        drought_tolerance=drought_tolerance,
                        fertility_requirement=fertility_requirement,
                        soil_ph_min=soil_ph_min,
                        soil_ph_max=soil_ph_max,
                        shade_tolerance=shade_tolerance)

        # We need to add to the session or it won't ever be stored
        db.session.add(plant)

    # Once we're done, we should commit our work
    db.session.commit()


def load_alerts():
    print 'Alerts'

    AlertType.query.delete()
    

    for i, row in enumerate(open('seed_data/alerts.txt')):
        row = row.rstrip()
        alert_type = row.split()
        alert = AlertType(alert_type=alert_type)

        db.session.add(alert)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_plants()
    load_alerts()

