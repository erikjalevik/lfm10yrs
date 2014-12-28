import sys, csv, datetime, sqlite3
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

stem = "http://ws.audioscrobbler.com/2.0/?"
apiKey = "05dba5b84d2a03c0f7821f4e97c33ac2"


def queryArtistTags(artist):

  params = {
    "method": "artist.gettoptags",
    "artist": artist,
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
    if int(count) > 0:
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

  result = c.execute("SELECT id, name FROM artist WHERE id NOT IN (SELECT artist_id FROM artist_tag) ORDER BY name");
  for row in result.fetchall():
    artistId = row[0]
    artist = row[1]
    tags = queryArtistTags(artist)
    
    for tag in tags:
      name = tag[0]
      count = tag[1]
    
      print("{0}: {1}: {2}".format(artist, name, count).encode("ascii", "ignore"))
    
      # Tag table
      c.execute("INSERT OR IGNORE INTO tag (name) VALUES (?)", (name,))
    
      # Artist Tag table
      c.execute("SELECT id FROM tag WHERE name=?", (name,))
      tagId = c.fetchone()[0]
      c.execute("INSERT OR IGNORE INTO artist_tag (artist_id, tag_id, count) VALUES (?, ?, ?)", (artistId, tagId, count))

    conn.commit()

  conn.close()
 
    
if __name__ == '__main__':
  main()

    
    
    
    
    
    
      #london = datetime.timedelta(hours = +0);
      #berlin = datetime.timedelta(hours = +1);
      #dt = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(london))
      
      #dateString = "{0}/{1}/{2} {3:02d}:{4:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
      #titleString = "{0} - {1}".format(line[4], line[2]) #.encode("ascii", "ignore")
