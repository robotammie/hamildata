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