function generateBars(reference, pos_data, callback) { 
  
  $(reference).empty()

  var margin = {top: 20, right: 20, bottom: 30, left: 40}
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
      .rangeRound([height, 0]);

  var color = d3.scale.ordinal()
      .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

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

  ////////////////////////////////////////////////////////////////////////

  d3.json("/bar_data.json", function(error, data) {
    if (error) throw error;

    if (pos_data !== null) {
      data = pos_data
    };

    infoData = data.data.infobox;

    // debugger;

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

generateBars('#chart');


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