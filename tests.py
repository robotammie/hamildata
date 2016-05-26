import unittest
from server import app
from model import Line, Song, Character, connect_to_db, db
from comparisons import comp_songs, make_json


class BasicTests(unittest.TestCase):
    """Flask tests that do not use the database."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")  # <- response object
        self.assertIn("Hamilton Data", result.data)
        print "Tested Homepage"

    # def test_no_rsvp_yet(self):
    #     # FIXME: Add a test to show we see the RSVP form, but NOT the party details
    #     result = self.client.get("/")
    #     self.assertIn("RSVP", result.data)
    #     self.assertNotIn("123 Magic Unicorn Way", result.data)
    #     print "Tested No RSVP"

    # def test_rsvp(self):
    #     # FIXME: Once we RSVP, we should see the party details, but not the RSVP form
    #     result = self.client.post("/rsvp",
    #                               data={'name': "Jane", 'email': "jane@jane.com"},
    #                               follow_redirects=True)
    #     self.assertNotIn("RSVP", result.data)
    #     self.assertIn("123 Magic Unicorn Way", result.data)
    #     print "Tested RSVP Form"


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    # def test_games(self):
    #     #FIXME: test that the games page displays the game from example_data()
    #     result = self.client.get("/games")
    #     self.assertIn("Galaxy", result.data)
    #     print "Tested Game List"


if __name__ == "__main__":
    unittest.main()



if __name__ == "__main__":
    unittest.main()
