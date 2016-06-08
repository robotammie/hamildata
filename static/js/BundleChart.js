//////////////////////////////////////////////////
// code template for bundle layout based on     //
// https://github.com/d3/d3/wiki/Bundle-Layout  //
//////////////////////////////////////////////////


function generateBundles(reference, callback) {

    // $('h3').html('Song Connections');
    $(reference).empty();
    $('h3').html("");
    $('#chart')
        .removeClass('chart-bar')
        .addClass('chart-bundle');
    $('#info-box')
        .removeClass('info-bar')
        .addClass('info-bundle info-none')
        .html('<h4>Click on a song title to see with which songs it shares lyrics.</h4>');


  //   // VARIABLE INSTANTIATION

    var diameter = 600, // dimensions of svg element
        radius = diameter / 2,
        innerRadius = radius - 160; // relative dimention of chart

    var cluster = d3.layout.cluster()
        .size([360, innerRadius]) // how many degrees, radius
        .sort(null)

    var bundle = d3.layout.bundle(); // bundle layout

    var line = d3.svg.line.radial()
        .interpolate("bundle")
        .tension(.1) // 0 is straight, 1 is super-curved
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    var svg = d3.select(reference).append("svg")
        .attr("id", "graph")
        .attr("viewBox", "10 1 515 575")
        .attr("preserveAspectRatio", "xMidYMid")
        .append("g")
        .attr("transform", "translate(" + (radius - 40) + "," + (radius + 10) + ")"); // center the graph in the svg element

    var link = svg.append("g").selectAll(".link"),
        node = svg.append("g").selectAll(".node");


    // BEGIN CODE

    // import json;  use data to 
    d3.json("/bundle_data.json", function(error, data) {
      if (error) throw error;

      var nodes = cluster.nodes(packageHierarchy(data.data)),
          links = packageImports(nodes);

      link = link
          .data(bundle(links))
          .enter().append("path")
          .each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
          .attr("class", "link")
          .attr("d", line);

      node = node
          .data(nodes.filter(function(n) { return !n.children; }))
          .enter().append("text")
          .attr("class", "node")
          // .attr("data", function(d) {console.log(d); return d})
          .attr("dy", ".31em") // center text on node
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")" + 
                                                  "translate(" + (d.y + 8) + ",0)" + 
                                                  (d.x < 180 ? "" : "rotate(180)"); 
                                          })
          .style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          .text(function(d) { return d.key; })
          .on("mouseover", mouseovered)
          .on("mouseout", mouseouted)
          .on("click", clicked);

      callback && callback(); // check if a callback exists, then run it
    });

    function mouseovered(d) {
      if ($('.node--song1').length === 0) {
          node
              .each(function(n) { n.target = n.source = false; }); // deletes previous source/target matching

          link
              .classed("link--target", function(l) { if (l.target === d) return l.source.source = true; })
              .classed("link--source", function(l) { if (l.source === d) return l.target.target = true; })
              .filter(function(l) { return l.target === d || l.source === d; })
              .each(function() { this.parentNode.appendChild(this); });

          d3.select(this)
              .classed("node--hover", true);

          node
              .classed("node--target", function(n) { return n.target; })
              .classed("node--source", function(n) { return n.source; });
      }
    }

    function mouseouted(d) {
      // un-highlight all links
      link
          .classed("link--target", false)
          .classed("link--source", false);

      // unhighlight all nodes
      node
          .classed("node--hover", false)
          .classed("node--target", false)
          .classed("node--source", false);
    }

    function clicked(d) {
      // if no nodes are currently selected
      if ($('.node--song1').length === 0) {
        d3.select(this)
          .classed("node--song1", true); // add song1 class (show lyrics)
      }

      // if the node is currently selected (as either song1 or song2)
      else if (d3.select(this)[0][0]
                   .outerHTML
                   .indexOf('node--song') > -1) {
        
        d3.select(this)
          .classed("node--song1", false); // remove song1 class
        d3.select(this)
          .classed("node--song2", false); // remove song2 class

        // un-highlight all links
        link
          .classed("link-song1-target", false)
          .classed("link-song1-source", false);

        link
          .classed("link-song12-target", false)
          .classed("link-song12-source", false)

        // unhighlight all nodes
        node
          .classed("node-song1-target", false)
          .classed("node-song1-source", false);

        // if song 2 exists, re-class it to song 1
        if ($('.node--song2').length === 1) {
          var song2 = d3.select('.node--song2');
          song2.classed("node--song2", false);
          song2.classed("node--song1", true);
        }
      }
      // if there is a song 1 already, but no song 2
      else if ($('.node--song2').length === 0) {
        d3.select(this)
          .classed("node--song2", true); // add song2 class (compare)
      }
      
      // if there is a song1, and is not a song2, show song1's lyrics
      if ($('.node--song2').length === 0 && $('.node--song1').length === 1) {
        
        $('#info-box').removeClass("info-none")

        node
          .each(function(n) { n.target = n.source = false; }); // deletes previous source/target matching?

        // select data attached to the song 1 node
        song1_d = $('.node--song1')[0]['__data__'];

        // highlight the links whose target/source matches the song1 data
        link
          .classed("link-song1-target", function(l) { if (l.target === song1_d) return l.source.source = true; })
          .classed("link-song1-source", function(l) { if (l.source === song1_d) return l.target.target = true; })
          .filter(function(l) { return l.target === song1_d || l.source === song1_d; })
          .each(function() { this.parentNode.appendChild(this); });

        node
          .classed("node-song1-target", function(n) { return n.target; })
          .classed("node-song1-source", function(n) { return n.source; });

        // pull the song title from the node label and create a heading for the info box.
        var title = d3.select('.node--song1')[0][0].innerHTML;
        $('#info-box').html('<h4 class="song-title">' + title + '</h4 >');

        // AJAX request to server to get character:lyric pairs for given title
        $.get('/get_lyrics.json',
              {'title': title},
              function(results){
                  // initialize empty string
                  var songLyrics = '<table id="lyrics">'
                  // add a new row containing the character name and lyrics for each line
                  for (var i = 0; i < results.lyrics.length; i++) {
                    songLyrics = songLyrics.concat('<tr>', 
                                                      '<td class="char">', 
                                                        results.lyrics[i][0], ': ',
                                                      '</td>', 
                                                      '<td class="lyrics">', 
                                                        results.lyrics[i][1], 
                                                      '</td>', 
                                                   '</tr>');
                    };
                  // insert newly created list of rows into table tags
                  $('#info-box').append(songLyrics, '</table>');
                });
      }
      // if two songs are selected, show common lyrics
      else if ($('.node--song1').length === 1 && $('.node--song2').length === 1) {

        $('#info-box').removeClass("info-none")
        
        // select data attached to the song 1 node
        song1_d = $('.node--song1')[0]['__data__'];
        song2_d = $('.node--song2')[0]['__data__'];


        link
          .classed("link-song1-target", false)
          .classed("link-song1-source", false);

        // highlight the links whose target/source matches the song1 data
        link
          .classed("link-song12-target", function(l) { if (l.target === song1_d && l.source === song2_d) return l.source.source = true; })
          .classed("link-song12-source", function(l) { if (l.source === song1_d && l.target === song2_d) return l.target.target = true; })
          .filter(function(l) { return l.target === song1_d || l.source === song1_d; })
          .each(function() { this.parentNode.appendChild(this); });

        // unhighlight all other nodes 9not song 1 or song 2)
        node
          .classed("node-song1-target", false)
          .classed("node-song1-source", false);

        // populate table header with both song titles
        var title1 = d3.select('.node--song1')[0][0].innerHTML;
        var title2 = d3.select('.node--song2')[0][0].innerHTML;
        $('#info-box').html('<div class="container match">'
                              + '<div class="one-song">'
                                + '<h4 class="song-title">'
                                  + title1
                                + '</h4>'
                              + '</div>'
                              + '<div class="one-song">'
                                + '<h4 class="song-title">'
                                  + title2
                                + '</h4>'
                              + '</div>'
                            + '</div>' // all titles
                            );

        $.get('/compare_songs.json', {'title1': title1, 'title2': title2}, function(results){

                                                    // do for every match found between song 1 and song 2
                                                    for (var match in results){
                                                      html = '<div class="container match">'
                                                      
                                                      var song1Lyrics = '<div class="one-song"><table id="lyrics">';
                                                      
                                                      // insert a new line into the song 1 table
                                                      for (var line in results[match].song1){
                                                        song1Lyrics = song1Lyrics.concat('<tr>', 
                                                                                            '<td class="char">', 
                                                                                              results[match].song1[line]['char'], ': ', 
                                                                                            '</td>', 
                                                                                            '<td class="lyrics">', 
                                                                                              results[match].song1[line]['line'], 
                                                                                            '</td>', 
                                                                                          '</tr>'
                                                                                         );
                                                        
                                                      }
                                                      html = html.concat(song1Lyrics, '</table></div>');
                                                      
                                                      // insert 1 line per matching lyric into song 2 table
                                                      var song2Lyrics = '<div class="one-song"><table id="lyrics">';
                                                      
                                                      for (var line in results[match].song2){
                                                        song2Lyrics = song2Lyrics.concat('<tr>', 
                                                                                            '<td class="char">', 
                                                                                              results[match].song2[line]['char'], ': ', 
                                                                                            '</td>', 
                                                                                            '<td class="lyrics">', 
                                                                                              results[match].song2[line]['line'], 
                                                                                            '</td>', 
                                                                                          '</tr>'
                                                                                         );
                                                      }
                                                      html = html.concat(song2Lyrics, '</table></div></div>');
                                                      
                                                      $('#info-box').append(html);
                                                    }

              });
      }
      // if no songs are selected
      else {
        $('#info-box').removeClass("info-double info-single").addClass("info-none");
        $('#info-box').html('<h4>Click on a song title to see with which songs it shares common lyrics.</h4>');
      }

      
    }


    d3.select(self.frameElement).style("height", diameter + "px");

    // Lazily construct the package hierarchy from class names.
    function packageHierarchy(classes) {
      var map = {};

      function find(name, data) {
        var node = map[name], i;
        if (!node) {
          node = map[name] = data || {name: name, children: []};
          if (name.length) {
            node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
            node.parent.children.push(node);
            node.key = name.substring(i + 1);
          }
        }
        return node;
      }

      classes.forEach(function(d) {
        find(d.name, d);
      });

      return map[""];
    }

    // Return a list of imports for the given array of nodes.
    function packageImports(nodes) {
      var map = {},
          imports = [];

      // Compute a map from name to node.
      nodes.forEach(function(d) {
        map[d.name] = d;
      });

      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.imports) d.imports.forEach(function(i) {
          imports.push({source: map[d.name], target: map[i]});
        });
      });

      return imports;
    }

}



//////////////////////////////////////////////////
//    code template for bar layout based on     //
//    https://bl.ocks.org/mbostock/3886208      //
//////////////////////////////////////////////////


function generateBarPage() {

  function generateBars(reference, pos_data, callback) { 
    
    $(reference).empty()
    $('#chart').removeClass('chart-bundle').addClass('chart-bar')
    $('#info-box').removeClass('info-bundle').addClass('info-bar')

    var margin = {top: 20, right: 20, bottom: 30, left: 40}
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#3b1300", "#601302", "#8a2b0e", "#c75e24", "#c79f58", 
                "#a4956a", "#868569", "#746f61", "#596160", "#607982"]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format("d"));

    var svg = d3.select(reference).append("svg")
        .attr("id", "graph")
        .attr("viewBox", "0 0 1050 650")
        .attr("preserveAspectRatio", "xMidYMid")
        // .attr("width", width + margin.left + margin.right)
        // .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // begin code

    d3.json("/bar_data.json", function(error, data) {
      if (error) throw error;

      if (pos_data !== undefined) {
        data = pos_data
      };

      infoData = data.data.infobox;

      data = data.data.graph;

      color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Song"; }));

      data.forEach(function(d) {
        var y0 = 0;
        d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
        d.total = d.ages[d.ages.length - 1].y1;
      });

      // data.sort(function(a, b) { return b.total - a.total; }); // do not sort data!

      x.domain(data.map(function(d) { return d.Song; }));
      
      if ( d3.max(data, function(d) { return d.total; }) > 5){
        y.domain([0, d3.max(data, function(d) { return d.total; })]);
      } else {
        y.domain([0, 5]);
      }

    
      // console.log(d3.max(data, function(d) { return d.total; }));

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")") 
          .call(xAxis)
        .selectAll("text")
          .attr("transform", "translate(-12,0) rotate(-60)")
          .style("text-anchor", "end")

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Number of Occurances");

      var song = svg.selectAll(".song")
          .data(data)
        .enter().append("g")
          .attr("class", "g")
          .attr("transform", function(d) { return "translate(" + x(d.Song) + ",0)"; });

      song.selectAll("rect")
          .data(function(d) { return d.ages; })
        .enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });

      var legend = svg.selectAll(".legend")
          .data(color.domain().slice())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(75," + i * 20 + ")"; });

      legend.append("rect")
          .attr("x", width - 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);

      legend.append("text")
          .attr("x", width - 24)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d; });

      // debugger;



      var results = '';

      for (var song in infoData) {

        results = results.concat('<div class="container">',
                                   '<h4 class="song-title">',
                                      infoData[song].title,
                                   '</h4>',
                                   '<table id="lyrics">');

        for (var line in infoData[song].lines){
          results = results.concat('<tr>', 
                                      '<td class="char">', 
                                        infoData[song].lines[line][0], ': ', 
                                      '</td>', 
                                      '<td class="lyrics">', 
                                        infoData[song].lines[line][1], 
                                      '</td>', 
                                    '</tr>');
        }

        results = results.concat('</table></div>');

      }

      $('#results').html(results);

    });

    callback && callback(); // check if a callback exists, then run it
    
  }

  function capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);

        callback && callback(); // check if a callback exists, then run it
        
  }

  generateBars('#chart') 

  $('h3').html('Alexander Hamilton');

  // create form
  $('#info-box').append("<div class='container'>" +
                          "<form id='searchbox'><label>" +
                            "Search for lyrics: " +
                            "<input type='text' name='search' value='look around'></label>" +
                            "<input type='submit' id='mybutton' value='Search'><br>" +
                            "<p class='form-instructions'>You can use \"%\" as a wildcard character. Example: \"Tell % story\"</p>" + 
                          "</form>" +
                        "</div>" +
                        "<div class='container' id='results'>" +
                        "</div>");

  // add event listener to form
  $(function(){
    $('#searchbox').submit(function (evt) {
        evt.preventDefault();
        // debugger;

        var formData = $('#searchbox').serializeArray();
        
        // debugger;

        $.get('/bar_data.json',
              formData,
              function(results){
                $('h3').html('"' + capitalizeFirstLetter(formData[0].value) + '"')
                generateBars('#chart', results);
              });
    });
  });

} // close create barChart/submitForm elements



// add event listeners to nav bar
$(function(){
  $('#song-connections').click(function (evt) {
      location.hash = ""
      $('#chart').empty();
      $('#info-box').empty();
    
      setupPage();
  });
});

$(function(){
  $('#search-lyrics').click(function (evt) {
      location.hash = "search"
      $('#chart').empty();
      $('#info-box').empty();

      setupPage();
  });
});

function setupPage() {
  if (location.hash === "#search") {
    generateBarPage("#chart");
    $('#li-lyrics').toggleClass( 'active', true );
    $('#li-connections').toggleClass( 'active', false );
    }
  else {
    generateBundles("#chart")
    $('#li-connections').toggleClass( 'active', true );
    $('#li-lyrics').toggleClass( 'active', false );
  };
}

setupPage();
