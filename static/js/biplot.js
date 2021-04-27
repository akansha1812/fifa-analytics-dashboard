function biplot(data,pca_line_data) {

$('#plot_area_scatter').empty();

var margin = {top: 10, right: 30, bottom: 30, left: 40},
    width = 800 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

var svg = d3.select("#plot_area_biplot")
  .append("svg")
    .attr("width", width + margin.left + margin.right + 20)
    .attr("height", height + margin.top + margin.bottom + 20)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


// Add X axis
  var x = d3.scaleLinear()
    .domain([-2, 2])
    .range([ 0, width ]);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("transform","translate(0,330)")
    .call(d3.axisBottom(x));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([-2, 2])
    .range([ height, 0]);
  svg.append("g")
  .attr("transform","translate(365,0)")
    .call(d3.axisLeft(y));

  // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
  // Its opacity is set to 0: we don't see it by default.
  var tooltip = d3.select("#plot_area")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px")

     // A function that change this tooltip when the user hover a point.
  // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
  var mouseover = function(d) {
    tooltip
      .style("opacity", 1)
  }

  var mousemove = function(d) {
    tooltip
      .html("The exact value on<br>the x-axis is: " + d['PC1'])
      .style("left", (d3.mouse(this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
      .style("top", (d3.mouse(this)[1]) + "px")
  }

  // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
  var mouseleave = function(d) {
    tooltip
      .transition()
      .duration(200)
      .style("opacity", 0)
  }

  // Add dots
  svg.append('g')
    .selectAll("dot")
    .data(data.filter(function(d,i){return i<500})) // the .filter part is just to keep a few dots on the chart, not all of them
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d['PC1']); } )
      .attr("cy", function (d) { return y(d['PC2']); } )
      .attr("r", 7)
      .style("fill", "#69b3a2")
      .style("opacity", 0.7)
      .style("stroke", "white")
    .on("mouseover", mouseover )
    .on("mousemove", mousemove )
    .on("mouseleave", mouseleave )

    svg.append("g").selectAll("line")
    .data(pca_line_data).enter().append("line")
    .attr("x1",x(0))
    .attr("x2", function(d) { 
        console.log(d.X)
        return  x(d.X)})
    .attr("y1",y(0))
    .attr("y2", function(d) { return y(d.Y)})
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-width", 1);

  svg.append("text")             
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("PC1");

  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("PC2"); 


}