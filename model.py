"""Models and database functions for Hamilton project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####################################################

class Line(db.Model):
    """A single line from one fo the songs"""

    __tablename__ = "lines"

    line_no = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    song_id = db.Column(db.Integer,
                        db.ForeignKey('song.song_id'),
                        nullable=False)
    char_code = db.Column(db.String(5),
                          db.ForeignKey('characters.char_code'),
                          nullable=False)
    lyrics = db.Column(db.String(128),
                       nullable=False)

    song = db.relationship('Song',
                           backref=db.backref('lines', order_by=line_no))

    char = db.relationship('Character',
                           backref=db.backref('characters', order_by=char_code))

    def __repr__(self):
        """define how model displays."""

        return "<Line %s.%s - %s>" % (self.song_id,
                                      self.line_no,
                                      self.lyrics)


class Song(db.Model):
    """A song from the musical Hamilton"""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String(64),
                      nullable=False)
    act = db.Column(db.Integer,
                    nullable=False)

    def __repr__(self):
        """define how model displays."""

        return "<Song %s. %s>" % (self.song_id,
                                  self.title)


class Character(db.Model):
    """A named character from the musical Hamilton"""

    __tablename__ = "characters"

    char_code = db.Column(db.String(5),
                          primary_key=True)
    full_name = db.Column(db.String(64),
                          nullable=False)
    name = db.Column(db.String(64),
                     nullable=False)

    def __repr__(self):
        """define how model displays."""

        return "<Char %s: %s>" % (self.char_code,
                                  self.name)


###############################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
