from jinja2 import StrictUndefined

from flask import Flask, render_template, jsonify, redirect, request, flash, session

from model import Line, Song, Character, connect_to_db, db

import json

# create fask application
app = Flask(__name__)

# cause Jinja to fail loudly, so errors are caught
# TODO: comment out before deployment
app.jinja_env.undefined = StrictUndefined


# route for homepage
@app.route('/')
def index():
    """Homepage."""

    # TODO: create dummy homepage

    return render_template("bundle_test.html")


@app.route("/data.json")
def get_graph_data():
    # call helper functions

    f = open('static/test_data.json')
    content = f.read()
    my_json = json.loads(content)

    print type(my_json)

    # nodes = make_nodes(f)
    # paths = make_paths(nodes)
    return jsonify({'data': my_json})


##########################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
