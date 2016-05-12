# Functions for use in Hamilton data project

from model import Line, connect_to_db
import re
import pprint


def compute_jaccard_index(s1, s2):
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

    for line1 in all_lines:
        # print line1.line_no
        for line2 in all_lines:
            if compute_jaccard_index(line1.lyrics, line2.lyrics) > .34:
                edges[line1] = edges.get(line1, [])
                edges[line1].append(line2)
    return edges


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    # print "Connected"

    # In case edge list hasn't been created, create it
    # edges = make_edge_list()
    # print "Created."

    pprint.pprint(make_edge_list())

else:
    print "Never ran."
