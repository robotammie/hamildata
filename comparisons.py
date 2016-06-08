# Functions for use in Hamilton data project

from model import Line, Song, Character, connect_to_db
import re
import json

sensitivity = .5


def compute_jaccard_index(s1, s2):
    """
    Use set math to determine percentage of words two strings have in common by
    dividing the number of words in common by number of total individual words.

    Function based off Tamim Shahriar's compute_jaccard_index, found at
    http://love-python.blogspot.com/2012/07/python-code-to-compute-jaccard-index.html'

    >>> compute_jaccard_index("little pig, little pig", "three little pigs")
    0.25

    >>> compute_jaccard_index("little red riding hood", "big bad wolf")
    0.0

    Uppercase and punctuation should be ignored; contractions should count
    as a single word, not two:
    >>> compute_jaccard_index("I'm a Little Teapot?", "Just a little.")
    0.4

    """
    # select individual punctuation marks because re non-alphanumeric includes '
    # need to exclude ' in order to keep contractions together
    # question mark goes first so it doesn't delete numbers (don't know why)
    # " and - must be escaped.
    set_1 = set(re.split("[?\s.,\-!\"]", s1.lower()))
    set_2 = set(re.split("[?\s.,\-!\"]", s2.lower()))

    # remove empty strings artifacts from punctuation
    set_1.discard('')
    set_2.discard('')
    set_1.discard('the')
    set_2.discard('the')

    # compute words in common between two strings
    common_words = len(set_1.intersection(set_2))
    # compute total individual words across both strings
    all_words = float(len(set_1) + len(set_2) - common_words)

    return common_words / all_words


def get_song_connections(song):
    """
    Create a list of songs with lyrical callbacks to the given song.

    """

    # initiate empty set (for duplicate checking)
    links = set([])

    # create lists of lines in the given song, and in all following songs
    lines = Line.query.filter(Line.song_id == song).all()
    all_lines = Line.query.filter(Line.song_id > song).all()

    # compare all lines in the given song to all other lones in the play
    for line1 in lines:
        for line2 in all_lines:
            # if they are lyrically similar, add the song number of the second song to our set of connectors
            if compute_jaccard_index(line1.lyrics, line2.lyrics) > sensitivity:
                links.add(str(line2.song.act) + '.' + line2.song.title)

    # return set to list form for future jsonification
    return list(links)


def make_json():
    """
    Create a list of dictionaries as required by d3 bundle layout

    """

    data = []

    # get song object, remember to add act # to name key:value pair
    songs = Song.query.all()

    for song in songs:
        # initiate an empty dictionary, and populate it
        mydict = {}
        mydict["name"] = str(song.act) + '.' + song.title
        mydict["imports"] = get_song_connections(song.song_id)

        data.append(mydict)

    f = open('static/song_data.json', 'w')
    f.write(json.dumps(data))


def comp_songs(song1, song2):
    """create a list of smilarities between two songs."""

    lines1 = Line.query.filter(Line.song_id == song1).all()
    lines2 = Line.query.filter(Line.song_id == song2).all()

    edges = {}

    used = {}

    for line1 in lines1:

        for line2 in lines2:
            if compute_jaccard_index(line1.lyrics, line2.lyrics) > sensitivity:
                print line2
                print used
                if line2.line_no not in used:

                    # add similar lines to the adjacency list
                    if edges.get(line1.line_no):    # line1 already has a match
                        edges[line1.line_no]['song2'][line2.line_no] = {'char': line2.char.name,
                                                                        'line': line2.lyrics
                                                                        }
                    else:                           # line1 does not have any matches yet
                        edges[line1.line_no] = {'song1': {line1.line_no: {'char': line1.char.name,
                                                          'line': line1.lyrics
                                                                          }
                                                          },
                                                'song2': {line2.line_no: {'char': line2.char.name,
                                                                          'line': line2.lyrics
                                                                          }
                                                          }
                                                }
                    used[line2.line_no] = line1.line_no
                    # print used

                else:
                    edges[used[line2.line_no]]['song1'][line1.line_no] = {'char': line1.char.name,
                                                                          'line': line1.lyrics
                                                                          }

    return edges


def get_bar_data(search_input):

    matches = (Line.query.filter(Line.lyrics.like("%" + search_input + "%") |
                                 Line.lyrics.like("%" + search_input.lower() + "%") |
                                 Line.lyrics.like("%" + search_input.capitalize() + "%"))
                         .order_by(Line.line_no).all())
    all_chars = {}

    # generate data for info box
    infobox_data = {}

    for line in matches:
        infobox_data[line.song_id] = infobox_data.get(line.song_id,
                                                      {'title': line.song.title, 'lines': []})
        infobox_data[line.song_id]['lines'].append((line.char.name,
                                                    line.lyrics))

    # generate data for bar graph
    graph_data = []

    # create dictionary of all characters who use the searched-for word
    all_chars = {}
    for line in matches:
        all_chars[line.char.name] = all_chars.get(line.char.name, 0)

    # create dictionary for each song, append character names
    songs = Song.query.order_by(Song.song_id).all()
    for song in songs:
        song_data = {'Song': song.title}
        song_data.update(all_chars)
        if song.song_id in infobox_data:
            for line in infobox_data[song.song_id]['lines']:
                char = line[0]
                song_data[char] += 1

        graph_data.append(song_data)

    route_data = {}
    route_data['graph'] = graph_data
    route_data['infobox'] = infobox_data

    return route_data


if __name__ == "__main__":
    """Create Adjacency List"""

    # connect to database
    from server import app
    connect_to_db(app)
    print "Connected"

    print "Generating adjacency dictionary..."
    make_json()
    print "Done."
