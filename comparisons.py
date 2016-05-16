# Functions for use in Hamilton data project

from model import Line, Song, Character, db, connect_to_db
import re
from pprint import pprint


def compute_jaccard_index(s1, s2):
    """
    Use set math to determine percentage of words two strings have in common by
    dividing the number of words in common by number of total individual words.

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

    # compute worsd in common between two strings
    common_words = len(set_1.intersection(set_2))
    # compute total individual words across both strings
    all_words = float(len(set_1) + len(set_2) - common_words)

    return common_words / all_words


def make_edge_list(str_list):
    """
    Create a dictionary of similar lines for visualization.

    Too complicated for a doctest.
    TODO: incorporate this into a unit test later
    """

    # initiate empty dictionary
    edges = {}

    for i in range(len(str_list)):
        line1 = str_list[i]
        # print line1
        # check only those lines after the one you're looking at
        # (to prevent duplicate matches)
        for line2 in str_list[i+1:]:
            # check jaccard similarity
            if compute_jaccard_index(line1.lyrics, line2.lyrics) >= .50:
                # add similar lines to the adjacency list
                edges[line1] = edges.get(line1, [])
                edges[line1].append(line2)
    return edges


def comp_songs(song1, song2):
    """create a list of smilarities between two songs."""

    lines1 = Line.query.filter(Line.song_id == song1).all()
    lines2 = Line.query.filter(Line.song_id == song2).all()

    edges = {}

    for line1 in lines1:
        for line2 in lines2:
            if compute_jaccard_index(line1.lyrics, line2.lyrics) >= .50:
                # add similar lines to the adjacency list
                edges[line1] = edges.get(line1, [])
                edges[line1].append(line2)
                # lines2.remove(line2)

    return edges





# song_lines = {i[0]: Line.query.filter(Line.song_id == i[0]).all() for i in db.session.query(Song.song_id).all()}

pprint(song_lines)

songnums = [17, 41]

if __name__ == "__main__":
    """Create Adjacency List"""

    # connect to database
    from server import app
    connect_to_db(app)
    print "Connected"
#     # create master list of all lines in database
#     all_lines = Line.query.all()
#     # Print the edge list (ideally to a txt file)
#     edges = (make_edge_list(all_lines))
#     pprint(edges)

else:
    print "Never ran."
