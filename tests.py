import unittest
from server import app
# from model import Line, Song, Character, example_data, connect_to_db, db
# from comparisons import comp_songs, make_json


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


# class PartyTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Do before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         # (uncomment when testing database)
#         db.session.close()
#         db.drop_all()

#     def test_chart(self):
#         """tests database-dependandt elements"""
#         result = self.client.get("/")
#         # self.assertIn("song1", result.data)
#         print "Tested chart creation"


if __name__ == "__main__":
    unittest.main()
