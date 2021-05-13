function wc(){


var xhr = new XMLHttpRequest();
var url = "http://localhost:5000/wc_filter";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        console.log("Response : ", data);
        wc(data);
    }
};
var filter = JSON.stringify({"age_start": age_start,"age_end": age_end,"country_name":country_name,
                             "value_start": value_start, "value_end":value_end,
                             "rating_start":rating_start, "rating_end":rating_end});
xhr.send(filter);

function wc(data) {

var myWords = data
// set the dimensions and margins of the graph
var margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 400 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
d3.select("#word_cloud svg").remove();
var svg = d3.select("#word_cloud").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
// Wordcloud features that are different from one word to the other must be here
var layout = d3.layout.cloud()
  .size([width, height])
  .words(myWords.map(function(d) { return {text: d.Name, size:d.Overall , c: d.c, id: d.ID}; }))
  .padding(2)        //space between words
  .rotate(function() { return ~~(Math.random() * 2) * 90; })
  .fontSize(function(d) { return d.size; })      // font size of words
  .on("end", draw);
layout.start();

// This function takes the output of 'layout' above and draw the words
// Wordcloud features that are THE SAME from one word to the other can be here


function draw(words) {
console.log(" print data : ")
console.log(words)

var color = d3.scaleOrdinal(d3.schemeCategory10);
  svg
    .append("g")
      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size; })
        .style("fill", function(d) { return color(d.c); })
        .attr("text-anchor", "middle")
        .style("font-family", "Impact")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
        .on('click', function(d) {
        console.log("Id AND Name : ",d.id,' , ',d.text )
        createSpiderChart(d.id,d.text)
        pitch_plot(d.id)
        player_card(d.id)});
}

}
// List of words

}