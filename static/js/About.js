function generateAbout(reference, callback) {

    $("h3").html("");

    $(reference).html('<br>' +
                      '<h4>What is Hamildata?</h4>' +
                      '<p>Hamildata provides users with visualizations of the way songs in the musical Hamilton reference one another. Songs are displayed on a bundle-layout graph that shows which songs share lyrical similarity. Users can select any two songs to see a list of lyrically similar lines. Additionally, users can also enter a word or phrase into a search box to get a list of all instances of that phrase across all songs, as well as a bar chart visualization of which characters used the phrase in which songs.</p>' +
                      '<p>It was written as my final project at Hackbright Academy, a coding bootcamp in San Francisco.</p>' +
                      '<br>' +
                      '<h4>Are you affiliated with the musical Hamilton at all?</h4>' +
                      '<p>Nope, just a fan (though I do hope to see it when they come to San Francisco next year).</p>' +
                      '<br>' +
                      '<h4>Why aren\'t [lines] shown as connected?</h4>' +
                      '<p>Hamildata uses a Jaccard Index to compare lines, which means that similarity is defined merely as having a certain percentage of words in common. This results, in some cases, in some lines being overlooked.</p>' +
                      '<p>For example:</p>' +
                      '<p>"We are waiting in the wings for you" and "When America sings for you" share only 2 words in common, and are not considered a match, while "We are waiting in the wings for you" and "Troops are waiting in the field for you" share 6 words in common, and are matched.</p>' +
                      '<br>' +
                      '<h4>What language(s) is it written in?</h4>' +
                      '<p>Database: PostgreSQL, with SQLAlchemy</p>' +
                      '<p>Back End: Python/Flask</p>' +
                      '<p>Front End: Javascript, including jQery and D3 libraries</p>' +
                      '<br>' +
                      '<h4>Can I play with your dataset/code?</h4>' +
                      '<p>Sure! All the code for this app, including the full lyrics listing, can be found at <a href="https://github.com/tkahnhau/hamildata">https://github.com/tkahnhau/hamildata</a></p>' +
                      '<br>' +
                      '<br>' +
                      '<h4>References and other links:</h4>' +
                      '<p><a href="http://www.hamiltonbroadway.com/">Official Hamilton Site</a></p>' +
                      '<p><a href="http://atlanticrecords.com/HamiltonMusic/">Official Hamilton Soundtrack page</a>, including links to the full lyrics .pdf and the Rap Genius pages for individual songs.</p>' +
                      '<p><a href="http://graphics.wsj.com/hamilton/">Wall Street Journal Article</a> comparing Hamilton lines on rhyme scheme rather than whole words</p>'

        );

}