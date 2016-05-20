//////////////////////////////////////////////////
// code template for bundle layout based on     //
// https://github.com/d3/d3/wiki/Bundle-Layout  //
//////////////////////////////////////////////////


// VARIABLE INSTANTIATION

var diameter = 600, // dimensions of svg element
    radius = diameter / 2,
    innerRadius = radius - 120; // relative dimention of chart

var cluster = d3.layout.cluster()
    .size([360, innerRadius]) // how many degrees, radius
    .sort(null)
    // .value(function(d) { return d.size; }); // this line doesn't seem to do anything

var bundle = d3.layout.bundle(); // bundle layout

var line = d3.svg.line.radial()
    .interpolate("bundle")
    .tension(.1) // 0 is straight, 1 is super-curved
    .radius(function(d) { return d.y; })
    .angle(function(d) { return d.x / 180 * Math.PI; });

var svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .append("g")
    .attr("transform", "translate(" + radius + "," + radius + ")"); // center the graph in the svg element

var link = svg.append("g").selectAll(".link"),
    node = svg.append("g").selectAll(".node");


// BEGIN CODE

// import json
d3.json("/data.json", function(error, data) {
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
      .attr("dy", ".31em") // center text on node
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
      .style("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .text(function(d) { return d.key; })
      .on("mouseover", mouseovered)
      .on("mouseout", mouseouted)
      .on("click", clicked);
});

function mouseovered(d) {
  node
      // .each(function(n) { n.target = n.source = false; });

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

function mouseouted(d) {
  link
      .classed("link--target", false)
      .classed("link--source", false);

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
    if ($('.node--song2').length === 1) {
      var song2 = d3.select('.node--song2');
      song2.classed("node--song2", false);
      song2.classed("node--song1", true);
    }
  }
  else if ($('.node--song2').length === 0) {
    d3.select(this)
      .classed("node--song2", true); // add song2 class (compare)
  }
  
  // node
  //     .classed("node--song1", false);

  // console.log(d3.select(this)[0][0].outerHTML.indexOf('node--song') > -1);

  // d3.select(this)
  //     .classed("node--song1", true); // give the selected node a class of node--select

  console.log(d3.select(this)[0][0].outerHTML.indexOf('node--song') > -1);
  
  // if there is a song1, and is not a song2, show song1's lyrics
  if ($('.node--song1').length !== 0 && $('.node--song2').length === 0) {
    
    // pull the song title from the node label and create a heading for the info box.
    var title = d3.select('.node--song1')[0][0].innerHTML;
    $('#info-box').html('<h4>' + title + '</h4 class="song-title">' + '<table id="lyrics"></table>');

    // AJAX request to server to get character:lyric pairs for given title
    $.get('/get_lyrics.json', {'title': title}, function(results){
                                                // initialize empty string
                                                var songLyrics = ''
                                                // add a new row containing the character name and lyrics for each line
                                                for (var i = 0; i < results.lyrics.length; i++) {
                                                  songLyrics = songLyrics.concat('<tr><td>', results.lyrics[i][0], ':</td><td>', results.lyrics[i][1], '</td></tr>')
                                                  };
                                                // insert newly created list of rows into table tags
                                                $('#lyrics').append(songLyrics);
                                                });
  }
  else {
    $('#info-box').html('');
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
