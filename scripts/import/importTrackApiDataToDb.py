import sys, csv, datetime, sqlite3
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

stem = "http://ws.audioscrobbler.com/2.0/?"
apiKey = "05dba5b84d2a03c0f7821f4e97c33ac2"


def queryTrack(artist, track):

  params = {
    "method": "track.getinfo",
    "artist": artist,
    "track": track,
    "api_key": apiKey
  }

  url = stem + urllib.parse.urlencode(params)

  response = urllib.request.urlopen(url).read()
  
  xmlTree = ET.fromstring(response)

  duration = xmlTree.findtext("track/duration")
  listeners = xmlTree.findtext("track/listeners")
  playcount = xmlTree.findtext("track/playcount")

  return (duration, listeners, playcount)

  
def main():

  args = sys.argv[1:]
  if not args:
    print("Usage: %s dbfile" % sys.argv[0])
    return

  dbFilename = args[0]
  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  result = c.execute("SELECT a.name, t.title, t.id FROM track t, artist a WHERE t.artist_id=a.id AND t.listeners IS NULL ORDER BY t.title")

  for row in result.fetchall():
    artist = row[0]
    track = row[1]
    trackId = row[2]
    (duration, listeners, playcount) = queryTrack(artist, track)
    
    print("{0} - {1}: {2} listeners, {3} plays, {4} duration".format(artist, track, listeners, playcount, duration).encode("ascii", "ignore"))
    
    c.execute("UPDATE track SET listeners=?, plays=?, duration=? WHERE id=?", (listeners, playcount, duration, trackId))
    conn.commit()

  conn.close()
  
    
if __name__ == '__main__':
  main()

    
    
    
    
    
    
      #london = datetime.timedelta(hours = +0);
      #berlin = datetime.timedelta(hours = +1);
      #dt = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(london))
      
      #dateString = "{0}/{1}/{2} {3:02d}:{4:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
      #titleString = "{0} - {1}".format(line[4], line[2]) #.encode("ascii", "ignore")
