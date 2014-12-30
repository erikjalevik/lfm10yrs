// To test locally in Chrome with cross-domain prevention disabled:
// chrome.exe --user-data-dir="J:/Dump/chrometestsession" --disable-web-security

d3.tsv("data/top50ArtistsScrobblesByYear.tsv", function (data)
{
  // This function will be called on completion of file read.
  // data is an array of objects keyed on column name.
  
/*
  var groupedData = d3.nest()
    .key(function(d) { return d.Artist })
    .key(function(d) { return d.Year })
    .rollup(function(leaves) { return parseInt(leaves[0].Scrobbles) })
    .map(data);
  console.log(groupedData)
*/
  var summedCounts = d3.nest()
    .key(function(d) { return d.Artist })
    .rollup(function(years) { return d3.sum(years.map(function(obj) { return parseInt(obj.Scrobbles) })) })
    .entries(data)
  summedCounts = summedCounts.map(function(obj) { return {artist: obj.key, scrobbles: obj.values} })

  var data = summedCounts

  var margin = {top: 20, right: 20, bottom: 20, left: 20}

  var svg = d3.select(".chart svg")
  var width = svg.attr("width") - margin.left - margin.right
  var height = svg.attr("height") - margin.top - margin.bottom

  var getValues = function(obj) { return obj.scrobbles }

  // Ordinal scales used for continuous values
  var scaleX = d3.scale.linear()
    .domain([0, d3.max(data, getValues)])
    .rangeRound([0, width])

  // Ordinal scales used for categories
  var scaleY = d3.scale.ordinal()
    .domain(d3.range(0, data.length))
    .rangeRoundBands([0, height], 0.05) // "round" forces integers, avoids anti-aliasing, but adds outer margins
    //.rangeBands([0, height], 0.05)

  var scaleColor = d3.scale.linear()
    .domain([0, d3.mean(data, getValues), d3.max(data, getValues)])
    .range(["#ffb832", "#e0884c", "#c61c6f"])

  // Creation
  var chart = svg.append("g")
    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")" )  

  var bars = chart.selectAll("g")
    .data(data)
    .enter()
    .append("g")
      .attr("transform", function(d, i) { return "translate(0," + scaleY(i) + ")" })
      .style("opacity", 0.0)
      //.attr("y", function(d, i) { return i * barHeight }) // doesn't work

  var rects = bars.append("rect")
    .attr("width", 0.0)
    .attr("height", scaleY.rangeBand())
    .style("fill", function(d) { return scaleColor(d.scrobbles) })

  var labels = bars.append("text")
    .attr("x", margin.left)
    .attr("y", scaleY.rangeBand() / 2)
    .attr("dy", "0.35em")
    .style("font-size", "14px")
    .style("fill", function(d) { return scaleColor(d.scrobbles) })
    .style("opacity", 0.0)
    .text(function(d) { return d.scrobbles })

  // In animations
  bars.transition().duration(1000)
    .style("opacity", 1.0)
    .delay(function(d, i) { return i * 20 })

  rects.transition().duration(1000)
    .ease("elastic", 1.0, 0.3) //  1st param = amplitude around final pos, 2nd param = inertia
    .attr("width", function(d) { return scaleX(d.scrobbles) })
    .delay(function(d, i) { return i * 20 })

  labels.transition().duration(1000)
    .ease("cubic-out")
    .attr("x", function(d) { return scaleX(d.scrobbles) - 30 })
    .style("fill", "#000000")
    .style("opacity", 1.0)
    .delay(function(d, i) { return 200 + i * 20 })

  var tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("padding", "0 10px")
    .style("background", "#ffffff")
    .style("opacity", 0.0)

  // Events
  rects.on("mouseover", function(d, i)
    {
      var rect = d3.select(this)

      rect.transition().duration(100)
        .style("fill", "#b1c0c0")

      // Use if positioning tooltip relative to bars
      //var rectW = parseInt(rect.attr("width"))
      //var rectH = parseInt(rect.attr("height"))

      tooltip.html(d.artist)
      tooltip.transition().duration(100)
        .style("opacity", 0.9)
    })

  rects.on("mouseout", function(d)
    {
      d3.select(this)
        .transition().duration(400)
        .style("fill", function(d) { return scaleColor(d.scrobbles) })

      tooltip.transition().duration(400)
        .style("opacity", 0.0)
    })

  d3.select("body").on("mousemove", function()
    {
      tooltip
        .style("left", d3.event.pageX + "px")
        .style("top", (d3.event.pageY + 24) + "px")
    })

});
