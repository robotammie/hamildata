"""Models and database functions for Hamilton project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####################################################

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


class Line(db.Model):
    """A single line from one fo the songs"""

    __tablename__ = "lines"

    # table data
    line_no = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    song_id = db.Column(db.Integer,
                        db.ForeignKey('songs.song_id'),  # foreign key
                        nullable=False)
    char_code = db.Column(db.String(5),
                          db.ForeignKey('characters.char_code'),  # foreign key
                          nullable=False)
    lyrics = db.Column(db.String(128),
                       nullable=False)

    # link models to one another for easier querying
    song = db.relationship('Song',
                           backref=db.backref('lines', order_by=line_no))
    char = db.relationship('Character',
                           backref=db.backref('lines', order_by=char_code))

    def __repr__(self):
        """define how model displays."""

        return "<Line %s.%s - %s>" % (self.song_id,
                                      self.line_no,
                                      self.lyrics)


###############################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hamildata'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
