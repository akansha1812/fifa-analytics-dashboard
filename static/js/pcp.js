function pcp(cust_dimensions){

$('#plot_area_pcp').empty();

var margin = {top: 50, right: 50, bottom: 50, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scaleBand().range([0, width], 1),
    y = {},
    dragging = {};

var line = d3.line(),
    axis = d3.axisLeft(),
    background,
    foreground;

var svg = d3.select("#plot_area_pcp").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("../static/asteroid_clustered_small.csv", function(error, data) {
// var dimensions = []
if(cust_dimensions.length<=1){
  dimensions = d3.keys(data[0]);
  console.log(dimensions);
}
else
{
  dimensions = cust_dimensions;
  console.log(dimensions);
}
dimensions = dimensions.filter(function(d) {
    return d != "cluster_label" && (y[d] = d3.scaleLinear()
        .domain(d3.extent(data, function(p) { return +p[d]; }))
        .range([height, 0]));
  })
  // Extract the list of dimensions and create a scale for each.
  x.domain(dimensions);
  //console.log(dimensions)

  // Add grey background lines for context.
  background = svg.append("g")
      .attr("class", "background")
    .selectAll("path")
      .data(data)
    .enter().append("path")
      .attr("d", path);

 var color = d3.scaleOrdinal(d3.schemeCategory10);

  // Add blue foreground lines for focus.
  foreground = svg.append("g")
      .attr("class", "foreground")
    .selectAll("path")
      .data(data)
    .enter().append("path")
      .attr("d", path)
      .style("stroke", function(d) { return color(d.cluster_label)});

  // Add a group element for each dimension.
  var g = svg.selectAll(".dimension")
      .data(dimensions)
    .enter().append("g")
      .attr("class", "dimension")
      .attr("transform", function(d) { 
        return "translate(" + x(d) + ")"; })
      .call(d3.drag()
        .subject(function(d) { return {x: x(d)}; })
        .on("start", function(d) {
          dragging[d] = x(d);
          background.attr("visibility", "hidden");
        })
        .on("drag", function(d) {
          dragging[d] = Math.min(width, Math.max(0, d3.event.x));
          foreground.attr("d", path);
          dimensions.sort(function(a, b) { return position(a) - position(b); });
          x.domain(dimensions);
          g.attr("transform", function(d) { return "translate(" + position(d) + ")"; })
        })
        .on("end", function(d) {
          delete dragging[d];
          transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
          transition(foreground).attr("d", path);
          background
              .attr("d", path)
            .transition()
              .delay(500)
              .duration(0)
              .attr("visibility", null);
        }));

  // Add an axis and title.
  g.append("g")
      .attr("class", "axis")
      .each(function(d) { d3.select(this).call(axis.scale(y[d])); })
    .append("text")
      .style("text-anchor", "middle")
      .attr("y", -9)
      .text(function(d) { 
        return d; })
      .attr("class","axis");

  g.append("g")
      .attr("class", "brush")
      .each(function(d) {
        d3.select(this).call(y[d].brush = d3.brushY().extent([[-10,0],[10,height]]).on("brush", brushed).on("end", brushEnd));
      })
    .selectAll("rect")
      .attr("x", -8)
      .attr("width", 16);
});

function position(d) {
  var v = dragging[d];
  return v == null ? x(d) : v;
}

function transition(g) {
  return g.transition().duration(500);
}

// Returns the path for a given data point.
function path(d) {
  return line(dimensions.map(function(p) { return [position(p), y[p](d[p])]; }));
}

activeBrushes= new Map();
function updateBrushing() {
    svg.selectAll("path").classed("hidden", d => {
      
      var path_visible = true;
      
      dimensions.forEach(attribute => {
        var attr_visible = true;
        if(activeBrushes.get(attribute) != undefined){
          const y0 = activeBrushes.get(attribute)[0]
          const y1 = activeBrushes.get(attribute)[1]
          const value = y[attribute](d[attribute])
          if(y0 <= value && y1 >= value){attr_visible = true;}
          else{attr_visible = false;}
        }
        path_visible = (path_visible && attr_visible);
      })
      
      return !path_visible;
    })
  }


function brushed(attribute) {
    activeBrushes.set(attribute, d3.event.selection);
    updateBrushing();
  }

  function brushEnd(attribute) {
    if (d3.event.selection !== null) return;
    activeBrushes.delete(attribute);
    updateBrushing();
  }

}