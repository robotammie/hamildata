"""Utility file to seed hamildatabase from data in data/"""
"""All data pulled from http://atlanticrecords.com/HamiltonMusic/
copyright Hmilton Broadway"""

from model import Line, Song, Character, connect_to_db, db
from server import app


def load_songs():
    """Load songs from songs.txt into database."""

    print "Songs"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    Song.query.delete()

    # Read songs.txt file and insert data
    for row in open("data/songs.txt"):
        row = row.rstrip()

        # unpack line into columns/fields
        title, act = row.split("\t")

        song = Song(title=title,
                    act=act)

        # add to session
        db.session.add(song)

    # session commit
    db.session.commit()


def load_characters():
    """Load movies from chars.txt into database."""

    print "Characters"

    Character.query.delete()

    for row in open("data/chars.txt"):
        row = row.rstrip()
        code, full_name, name = row.split("\t")

        char = Character(char_code=code,
                         full_name=full_name,
                         name=name)

        db.session.add(char)

    db.session.commit()


def load_lines():
    """Load lyrics from lines.txt into database."""

    print "Lines"

    Line.query.delete()

    for row in open("data/lines.txt"):
        row = row.rstrip()
        song_id, char_code, lyrics = row.split("\t")

        line = Line(song_id=song_id,
                    char_code=char_code,
                    lyrics=lyrics)

        # We need to add to the session or it won't ever be stored
        db.session.add(line)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    print "Connected"

    # In case tables haven't been created, create them
    db.create_all()
    print "Created"

    # Import different types of data
    load_songs()
    load_characters()
    load_lines()
else:
    print "Never ran."
