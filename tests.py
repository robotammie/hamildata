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
        self.assertIn("Hamilton Data", result.data)
        print "Tested Homepage"

    def test_song_data(self):
        result = self.client.get("/data.json")
        self.assertIn("Alexander Hamilton", result.data)
        print "Tested jsonified song data"


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

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


if __name__ == "__main__":
    unittest.main()
