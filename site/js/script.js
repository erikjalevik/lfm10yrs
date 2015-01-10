// To test locally in Chrome with cross-domain prevention disabled:
// chrome.exe --user-data-dir="J:/Dump/chrometestsession" --disable-web-security
//
// Or run python -m SimpleHTTPServer 8080 in the site directory.
// Or python -m http.server 8080 if the above doesn't work.

d3.tsv("data/top50ArtistsOverall.tsv", function (data)
{
  // This function will be called on completion of file read.
  // data is an array of objects keyed on column name.
  
  // xField - scrobbles
  // yField - artist
  barChart(data, "scrobbles", "artist")

})

d3.tsv("data/top50ArtistsScrobblesByYear.tsv", function (data)
{
  // xField - scrobbles
  // yField - artist
  // stackField - year
  //stackedBarChart(data, "scrobbles", "artist", "year")
})
