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

    return "When I grow up I want to be a webpage."
