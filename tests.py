import unittest
from server import app
from model import Line, Song, Character, example_data, connect_to_db, db
# from comparisons import comp_songs, make_json


class BasicTests(unittest.TestCase):
    """Flask tests that do not use the database."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")  # <- response object
        self.assertIn("Song Comparisons", result.data)
        print "Tested Homepage"

    def test_song_data(self):
        result = self.client.get("/bundle_data.json")
        self.assertIn("Alexander Hamilton", result.data)
        print "Tested jsonified song data"

    def test_route2(self):
        result = self.client.get("/2")  # <- response object
        self.assertIn("Search for lyrics:", result.data)
        print "Tested Route 2"


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///travis_ci_test")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_get_lyrics(self):
        result = self.client.get("/get_lyrics.json?title=song1")
        self.assertIn("Look around!", result.data)
        self.assertIn("Hamilton", result.data)
        print "Tested song lyrics request"

    def test_compare_songs(self):
        result = self.client.get("/compare_songs.json?title1=song1&title2=song2")
        self.assertIn("Look around!", result.data)
        self.assertIn("Burr", result.data)
        print "Tested song comparison request"

    def test_bar_data_lower(self):
        result = self.client.get("/bar_data.json?search=bastard")
        self.assertIn("orphan", result.data)
        self.assertIn("1", result.data)
        print "Tested bar data (lower) request"

    def test_bar_data_upper(self):
        result = self.client.get("/bar_data.json?search=Bastard")
        self.assertIn("orphan", result.data)
        self.assertIn("1", result.data)
        print "Tested bar data (upper) request"


if __name__ == "__main__":
    unittest.main()
