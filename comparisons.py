# Functions for use in Hamilton data project

from model import Line, Song, Character, db, connect_to_db
import re
from pprint import pprint
from difflib import SequenceMatcher


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


# def longest_match(s1, s2):
#     """determine the longest number of consecutive words in common"""

#     list1 = re.split("[?\s.,\-!\"]", s1.lower())
#     list2 = re.split("[?\s.,\-!\"]", s2.lower())

#     while '' in list1:
#         list1.remove('')

#     while '' in list2:
#         list2.remove('')

#     matcher = SequenceMatcher(None, list1, list2)

#     match = matcher.find_longest_match(0, len(list1), 0, len(list2))

#     return match.size


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
            # match = longest_match(line1.lyrics, line2.lyrics)
            # if match >= 2:

            # check jaccard similarity
            if compute_jaccard_index(line1.lyrics, line2.lyrics) == .50:

               # add similar lines to the adjacency list
                edges[line1] = edges.get(line1, [])
                edges[line1].append(line2)
                
    return edges


def comp_lines(song1, song2):
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


# def comp_songs():
#     """
#     Create a dictionary of similarities between songs.

#     """

#     song_ids = db.session.query(Song.song_id).all()

#     # create dictionary of song lines, sorted by song number
#     song_lines = {s[0]: Line.query.filter(Line.song_id == s[0]).all() for s in song_ids}

#     # initiate empty dictionary
#     edges = {}

#     for song_id1 in song_lines:
#         # for each item in the value list
#         edges[song_id1] = {}
#         skip = [song_id1]
#         for line1 in song_lines[song_id1]:
#             # for each key in song_lines THAT IS NOT SONG_ID1
#                 for song_id2 in song_lines:
#                     if song_id2 not in skip:
#                         # for each line in the value list
#                         for line2 in song_lines[song_id2]:
#                             # if the two lines match
#                             if compute_jaccard_index(line1.lyrics, line2.lyrics) >= .50:
#                                 # iterate edges[songnum1][songnum2] by one
#                                 # import pdb; pdb.set_trace()
#                                 edges[song_id1][song_id2] = edges[song_id1].get(song_id2, 0)
#                                 edges[song_id1][song_id2] += 1

#         return edges


if __name__ == "__main__":
    """Create Adjacency List"""

    # connect to database
    from server import app
    connect_to_db(app)
    print "Connected"

    all_lines = Line.query.all()
    # Print the edge list (ideally to a txt file)
    pprint(make_edge_list(all_lines))

else:
    print "Never ran."
