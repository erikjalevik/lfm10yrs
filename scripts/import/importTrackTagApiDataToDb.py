import sys, csv, datetime, sqlite3
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

stem = "http://ws.audioscrobbler.com/2.0/?"
apiKey = "05dba5b84d2a03c0f7821f4e97c33ac2"


def queryTrackTags(artist, track):

  params = {
    "method": "track.gettoptags",
    "artist": artist,
    "track": track,
    "api_key": apiKey
  }

  url = stem + urllib.parse.urlencode(params)

  response = urllib.request.urlopen(url).read()
  
  xmlTree = ET.fromstring(response)

  tagList = []
  
  tags = xmlTree.findall("toptags/tag")
  for tagNode in tags:
    name = tagNode.findtext("name")
    count = tagNode.findtext("count")
    if count.isdigit() and int(count) > 0:
      tagList.append((name.lower(), count))
    
  return tagList

  
def main():

  args = sys.argv[1:]
  if not args:
    print("Usage: %s dbfile" % sys.argv[0])
    return

  dbFilename = args[0]
  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  result = c.execute("SELECT a.name, t.title, t.id FROM track t, artist a " + \
                     "WHERE t.artist_id=a.id AND t.id NOT IN (SELECT track_id FROM track_tag) AND t.id > 18382 ORDER BY t.id")
  for row in result.fetchall():
    artist = row[0]
    track = row[1]
    trackId = row[2]
  
    print()
    print(trackId)

    tags = queryTrackTags(artist, track)
    
    print("{0}. {1} - {2}".format(trackId, artist, track).encode("ascii", "ignore"))

    for tag in tags:
      name = tag[0]
      count = tag[1]
    
      print("  {0}: {1}".format(name, count).encode("ascii", "ignore"))
    
      # Tag table
      c.execute("INSERT OR IGNORE INTO tag (name) VALUES (?)", (name,))
    
      # Track Tag table
      c.execute("SELECT id FROM tag WHERE name=?", (name,))
      tagId = c.fetchone()[0]
      c.execute("INSERT OR IGNORE INTO track_tag (track_id, tag_id, count) VALUES (?, ?, ?)", (trackId, tagId, count))

    conn.commit()

  conn.close()
 
    
if __name__ == '__main__':
  main()

    
    
    
    
    
    
      #london = datetime.timedelta(hours = +0);
      #berlin = datetime.timedelta(hours = +1);
      #dt = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(london))
      
      #dateString = "{0}/{1}/{2} {3:02d}:{4:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
      #titleString = "{0} - {1}".format(line[4], line[2]) #.encode("ascii", "ignore")
