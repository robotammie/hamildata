# Functions for use in Hamilton data project

from model import Line, connect_to_db
import re
import pprint


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
    # print set_1
    set_2 = set(re.split("[?\s.,\-!\"]", s2.lower()))
    # print set_2
    set_1.discard('')
    # set_1.discard('and')
    set_2.discard('')
    # set_2.discard('and')
    common_words = len(set_1.intersection(set_2))
    # print common_words
    all_words = float(len(set_1) + len(set_2) - common_words)
    # print all_words
    return common_words / all_words


def make_edge_list():
    edges = {}
    # print "Creating Edge List..."
    all_lines = Line.query.all()

    for i in range(len(all_lines)):
        line1 = all_lines[i]
        # print line1.line_no
        for line2 in all_lines[i+1:]:
            if compute_jaccard_index(line1.lyrics, line2.lyrics) > .34:
                edges[line1] = edges.get(line1, [])
                edges[line1].append(line2)
    return edges


# if __name__ == "__main__":
#     """Create Adjacency List"""

#     from server import app
#     connect_to_db(app)
#     print "Connected"

#     # Print the edge list (ideally to a txt file)
#     pprint.pprint(make_edge_list())

# else:
#     print "Never ran."
