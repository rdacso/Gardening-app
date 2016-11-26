import json
from unittest import TestCase
from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db, example_data
from server import app
import server