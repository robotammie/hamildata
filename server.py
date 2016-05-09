from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session

from model import Line, Song, Character, connect_to_db, db

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

    return render_template("homepage.html")


##########################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
