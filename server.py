import json

from jinja2 import StrictUndefined

from flask import Flask, render_template, jsonify, redirect, request, flash, session

from model import Line, Song, Character, connect_to_db, db

from comparisons import comp_lines



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
    song_lines = (Line.query
                  .filter(Line.song_id == (db.session.query(Song.song_id)  # check that the song id for the line is the same as the song id
                                           .filter(Song.title == song_title).one()  # for the song passed in by the AJAX query
                                           )[0])
                  .order_by(Line.line_no).all())  # sort by line number

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


@app.route("/compare_songs.json")
def compare_songs():
    """Get song lyrics to populate info box"""

    song_title_1 = request.args.get('title1')
    song_title_2 = request.args.get('title2')

    # get the song id for the line from the title passed in by the AJAX query
    song1 = db.session.query(Song.song_id).filter(Song.title == song_title_1).one()[0]
    song2 = db.session.query(Song.song_id).filter(Song.title == song_title_2).one()[0]

    comparisons = comp_lines(song1, song2)

    # TODO: rewrite comp_lines so that it returns a dictionary of tuples, as per notebook sketch

    return jsonify({0: {'song1': {'char': '1-char 1', 'line': '1-line 1'},
                        'song2': {0: {'char': '2-char 1', 'line': '2-line 1'},
                                  1: {'char': '2-char 2', 'line': '2-line 2'}}
                        },
                    1: {'song1': {'char': '1-char 2', 'line': '1-line 2'},
                        'song2': {0: {'char': '2-char 3', 'line': '2-line 3'}}
                        }
                    })


##########################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()

  