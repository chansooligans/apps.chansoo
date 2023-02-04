var widthMultiplier;
if (window.innerWidth < 500) {
    widthMultiplier = 0.9;
} else {
    widthMultiplier = 0.5;
}

// set the dimensions and margins of the graph
var margin = { top: 20, right: 30, bottom: 40, left: 120 },
    width = window.innerWidth * widthMultiplier - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
    .classed("mx-auto text-center", window.innerWidth > 500)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Parse the Data
d3.csv("/static/csv/summary.csv", function (data) {

    // Add X axis
    var x = d3.scaleLinear()
        .domain([-3, 4])
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Y axis
    var y = d3.scaleBand()
        .range([0, height])
        .domain(data.map(function (d) { return d["feature"]; }))
        .padding(.1);
    svg.append("g")
        .call(d3.axisLeft(y))

    //Bars
    svg.selectAll("myRect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", function (d) { return d["red=north"] >= 0 ? x(0) : x(d["red=north"]); })
        .attr("y", function (d) { return y(d["feature"]); })
        .attr("width", function (d) { return x(Math.abs(d["red=north"])) - x(0); })
        .attr("height", y.bandwidth())
        .attr("fill", "#69b3a2")


    // .attr("x", function(d) { return x(d.Country); })
    // .attr("y", function(d) { return y(d.Value); })
    // .attr("width", x.bandwidth())
    // .attr("height", function(d) { return height - y(d.Value); })
    // .attr("fill", "#69b3a2")

})

