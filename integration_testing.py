import json
import unittest
from model import connect_to_db, db, example_data
from server import app

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
        connect_to_db(app, "postgresql:///gardening")

        #create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_find_users(self):
        """Can we find an employee in the sample data?"""
        al = User.query.filter(User.first_name == 'Al').first()
        self.assertEqual(al.first_name, 'Al')



class UserLogin(unittest.TestCase):
    """Tests that do require db"""
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()

        #connect to test database
        connect_to_db(app, "postgresql:///gardening")



        #create tables and add sample data
        db.create_all()
        example_data()


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
                              data={"email": "al@test.com", "password": "admin123"},
                              follow_redirects=True)
        self.assertIn("Welcome Al", result.data)
        self.assertIn('rose', result.data)

    # def test_login_error_handling(self):
    #     """Test that user can't see important page when logged out."""

    #     result = self.client.get("/users/<user_id", 
    #                             data={'email': 'test@test.com', 'password':'fakeuser'},
    #                             follow_redirects=True)
    #     self.assertNotIn("Welcome Test", result.data)
    #     self.assertIn("No such user", result.data)

    # def test_existing_plants_display(self):
    #     result = self.client.get('/users')

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

class SessTesting(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key = "ABC"
        self.client = app.test_client()

        #connect to test database
        connect_to_db(app, "postgresql:///gardening")

        #create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1
  

    def test_logout(self):

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("healthy, happy garden", result.data)




    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()




if __name__ == "__main__":
    import unittest

    unittest.main()
