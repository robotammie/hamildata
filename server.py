from jinja2 import StrictUndefined

from flask import Flask, render_template, jsonify, redirect, request, flash, session

from model import Line, Song, Character, connect_to_db, db

import json

# create fask application
app = Flask(__name__)

# cause Jinja to fail loudly, so errors are caught
# TODO: comment out before deployment
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Render homepage."""

    return render_template("homepage.html")


@app.route("/data.json")
def get_graph_data():
    """pull pre-loaded song connections from json file"""

    # open pre-loaded file of song connections
    f = open('static/song_data.json')
    content = f.read()
    my_json = json.loads(content)

    # render json to homepage
    return jsonify({'data': my_json})


@app.route("/get_lyrics.json")
def get_lyrics():
    """Get song lyrics to populate info box"""

    # get song title frm AJAX request
    song_title = request.args.get('title')

    # find all song lines from the given song
    song_lines = (Line.query.filter(Line.song_id == (db.session.query(Song.song_id).filter(Song.title == song_title).one())[0]).order_by(Line.line_no).all())

    song_lyrics = []

    # pull character names and lyrics from the Line object
    for line in song_lines:
        # print line
        name = line.char.name
        lyrics = line.lyrics

        # append tuple to list of song lyrics
        song_lyrics.append((name, lyrics))

    # pass list of tuples back to webpage
    return jsonify({'lyrics': song_lyrics})


##########################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()

  