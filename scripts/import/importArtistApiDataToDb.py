import sys, csv, datetime, sqlite3
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

stem = "http://ws.audioscrobbler.com/2.0/?"
apiKey = "05dba5b84d2a03c0f7821f4e97c33ac2"


def queryArtist(artist):

  params = {
    "method": "artist.getinfo",
    "artist": artist,
    "api_key": apiKey
  }

  url = stem + urllib.parse.urlencode(params)

  response = urllib.request.urlopen(url).read()
  
  xmlTree = ET.fromstring(response)

  listeners = xmlTree.findtext("artist/stats/listeners")
  playcount = xmlTree.findtext("artist/stats/playcount")

  return (listeners, playcount)

  
def main():

  args = sys.argv[1:]
  if not args:
    print("Usage: %s dbfile" % sys.argv[0])
    return

  dbFilename = args[0]
  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  result = c.execute("SELECT name FROM artist WHERE listeners IS NULL ORDER BY name")

  for row in result.fetchall():
    artist = row[0]
    (listeners, playcount) = queryArtist(artist)
    
    print("{0}: {1} listeners, {2} plays".format(artist, listeners, playcount).encode("ascii", "ignore"))
    
    c.execute("UPDATE artist SET listeners=?, plays=? WHERE name=?", (listeners, playcount, artist))
    conn.commit()

  conn.close()
  
    
if __name__ == '__main__':
  main()

    
    
    
    
    
    
      #london = datetime.timedelta(hours = +0);
      #berlin = datetime.timedelta(hours = +1);
      #dt = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(london))
      
      #dateString = "{0}/{1}/{2} {3:02d}:{4:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
      #titleString = "{0} - {1}".format(line[4], line[2]) #.encode("ascii", "ignore")
