import json
import unittest
from model import User, UserPlant, PlantType, AlertType, Alert, connect_to_db, db, example_data
from server import app
import server

TEST_DATABASE_URI = "postgresql:///testingdb"

#Basic unit tests that do not involve the database.

class TestsForGuests(unittest.TestCase):
    """Tests that don't require the db."""

    # Get the Flask test client and data set up
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Welcome to Green Light!", result.data)
        self.assertNotIn("Logout", result.data)

    def test_login_page(self):
        result = self.client.get("/login")
        self.assertIn("Log In Here!", result.data)

    def test_register_page(self):
        result = self.client.get("/register")
        self.assertIn("Confirm Password", result.data)


#Unit tests that query the database for existing data
class FindDataInDb(unittest.TestCase):
    """tests that query the database"""

    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()

        #connect to test database
        connect_to_db(app, )

        #create tables and add sample data
        db.create_all()
        example_data()
        # print PlantType.query.get(1)
        print "done with FindDataInDb setup"

    def test_find_users(self):
        """Can we find a user in the sample data?"""
        al = User.query.filter(User.first_name == 'Ari').first()
        self.assertEqual(al.first_name, 'Ari')

    def test_find_plants(self):
        """Can we find a plant in the sample data?"""
        rose = PlantType.query.filter(PlantType.common_name == 'rose').first()
        self.assertEqual(rose.common_name, 'rose')

    def test_find_user_plants(self):
        """Can we find a user's plant in the sample data?"""
        rose = UserPlant.query.filter(UserPlant.plant_id == 1).first()
        self.assertEqual(rose.plant_id, 1)

    def test_find_alert_type(self):
        """Can we find an alert type in the sample data?"""
        watering = AlertType.query.filter(AlertType.alert_type == 'watering').first()
        self.assertEqual(watering.alert_type, 'watering')

    def test_find_alert(self):
        """Can we find a plant's alert in the sample data?"""
        watering = Alert.query.filter(Alert.user_plant_id == 1).first()
        self.assertEqual(watering.user_plant_id, 1)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

class UserLogin(unittest.TestCase):
    """Tests that do require db"""
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()


        #connect to test database
        connect_to_db(app, "postgresql:///testdb")

        #create tables and add sample data
        db.create_all()
        example_data()

        print "done with UserLogin setup"


    def test_register(self):
        result = self.client.post('/register',
                                    data={'first_name':'Joe', 
                                    'last_name':'Mommuh', 'email':'jm@test.com', 
                                    'phone_number':7132029974, 'password':'testuser', 
                                    'confirm_password':'testuser'},
                                    follow_redirects=True)
        self.assertIn('These are the plants in your garden!', result.data)


    def test_login(self):
        result = self.client.post("/login",
                              data={"email": "av@test.com", "password": "admin123"},
                              follow_redirects=True)
        self.assertIn("Welcome Ari", result.data)
        self.assertIn('rose', result.data)
        self.assertIn('watering', result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

class SessTesting(unittest.TestCase):
    """Tests that do require db"""
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()

        #connect to test database
        connect_to_db(app, "postgresql:///testdb")

        #create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1

    # def test_add_quantity(self):
    #     result = self.client.get('/addqty.json', data={'qty': 33, 'user_plant_id':1})
    #     self.assertIn("{'user_plant_id':1, 'qty':33}", result.data)

    def test_logout(self):

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("healthy, happy garden", result.data)

    # def test_add_plant(self):
    #     result = self.client.post('addplant', 
    #                             data={'common_name': 'bluebell'},
    #                             follow_redirects=True)
    #     self.assertIn('bluebell', result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

if __name__ == "__main__":
    # import unittest

    unittest.main()
