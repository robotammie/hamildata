# Hamilton Data Visualizer

[https://hamildata.herokuapp.com/](https://hamildata.herokuapp.com/)


### Overview

Hamildata provides visualizations of the lyrical overlap between songs in the musical *Hamilton*.

![Animation](http://i.imgur.com/rJprS7t.gif)

#####  Song Connections

On load, the site supplies the user with a bundle layout graph that shows which songs share lines in common. Users can select any song from the graph to highlight all its connections and get the lyrics for that song (populated via AJAX request in the info panel at right).

If the user selects a second song, the info panel shifts to display all lines that share similarity across both songs.

Similarity is determined via Jaccard Index, and is a function of what percentage of words across both lines are identical.

![Image](http://i.imgur.com/ryhrKjV.png)

#####  Search lyrics

A second route allows users to search the full text of the play to find all instances of a word or phrase across all songs. On search, the bar graph repopulates to show how many instances of the word/phrase appear in each song, color-coded by the character who sings it.

The info-box at right shows the full lines, divided by the song in which they appear.

It was created for my final project at Hackbright Academy. Hamildata is protected under the [MIT open source license](https://opensource.org/licenses/MIT).

### Running Locally

Although Hamildata is deployed online via heroku at [https://hamildata.herokuapp.com/](https://hamildata.herokuapp.com/), you can also run it locally.

#####  Setting Up Your Environment

Once you've downloaded the files from github, you will need to set up an environment with Python Flask and SQLAlchemy. 

Begin by setting up an virtual environment in the folder you downloaded the files to and activating it. Then install Flask, SQLAlchemy, and their dependencies by entering the below into your command line.

    pip install -r requirements.txt

#####  Database

You will also need to set up and populate a relational database. Instructions below are for PostgreSQL, but other relational databases may work as well.

Download [PostgreSQL](https://www.postgresql.org/) if you do not have it loaded already. Follow the instructions on the installer.

Once you have a database loaded, you need to create a database for this file and populate it with the data from the files provided.

In your command console, issue the following command:

    createdb hamildata

If you are using Postgres, you can populate it from the Posgres .dump file, which will load both the data and indexes.

    pg_restore -d hamildata hamildatabase.dump

Otherwise, you will need to seed the database manually by running seed.py. Indexes can be manually recreated from the code found in psql_indexes.sql.

    python seed.py

    psql hamildata
    hamildata=# CREATE INDEX song_lines ON lines (song_id);


#####  Running the server

Once your database is seeded, you can run your server by running

    python server.py

Your site should now be up and running locally.

Enjoy!




