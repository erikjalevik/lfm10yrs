import sys, csv, datetime, sqlite3

 
def main():

  args = sys.argv[1:]
  if not args:
    print("Usage: %s dbfile reportfile" % sys.argv[0])
    return

  dbFilename = args[0]
  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  reportFilename = args[1]
  file = open(reportFilename, "w", encoding="utf8", newline='')
  writer = csv.writer(file, delimiter="\t")
  writer.writerow(["Artist", "Year", "Scrobbles"]);

  # Get years
  #yearsResult = c.execute("SELECT strftime('%Y', datetime(timestamp, 'unixepoch')) AS year FROM scrobble GROUP BY year ORDER BY year")

  # Get all-time top 50
  topArtistsResult = c.execute(
    "SELECT a.id, count(s.id) AS scrobbles FROM scrobble s, track t, artist a " + \
    "WHERE s.track_id=t.id AND t.artist_id=a.id GROUP BY a.name ORDER BY scrobbles DESC LIMIT 50")

  for row in topArtistsResult.fetchall():
    artistId = row[0]
    
    scrobblesByYear = c.execute(
      "SELECT a.name, strftime('%Y', datetime(s.timestamp, 'unixepoch')) as year, count(s.id) AS scrobbles " + \
      "FROM scrobble s, track t, artist a " + \
      "WHERE s.track_id=t.id AND t.artist_id=a.id AND a.id=? GROUP BY year ORDER BY year",
      (artistId,))
    
    for row in scrobblesByYear.fetchall():
      artist = row[0]
      year = row[1]
      scrobbles = row[2]
      
      print("{0}, {1}, {2}".format(artist, year, scrobbles).encode("ascii", "ignore"))
      writer.writerow([artist, year, scrobbles]);

  conn.close()
  file.close()
  
    
if __name__ == '__main__':
  main()

