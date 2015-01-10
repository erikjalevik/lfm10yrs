import sys, csv, datetime, sqlite3
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

stem = "http://ws.audioscrobbler.com/2.0/?"
apiKey = "05dba5b84d2a03c0f7821f4e97c33ac2"


def queryInfo(tag):

  params = {
    "method": "tag.getinfo",
    "tag": tag.strip(),
    "api_key": apiKey
  }

  url = stem + urllib.parse.urlencode(params)

  response = urllib.request.urlopen(url).read()
  
  xmlTree = ET.fromstring(response)

  tagList = []
  
  reach = xmlTree.findtext("tag/reach")
  count = xmlTree.findtext("tag/taggings")

  return (reach, count)

  
def main():

  args = sys.argv[1:]
  if not args:
    print("Usage: %s dbfile" % sys.argv[0])
    return

  dbFilename = args[0]
  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  result = c.execute("SELECT id, name FROM tag WHERE reach IS NULL")
  for row in result.fetchall():
    tagId = row[0]
    tag = row[1]
  
    (reach, count) = queryInfo(tag)
    
    print("{0}. {1}: reach {2}, count {3}".format(tagId, tag, reach, count).encode("ascii", "ignore"))

    c.execute("UPDATE tag SET reach=?, count=? WHERE id=?", (reach, count, tagId))
    
    conn.commit()

  conn.close()
 
    
if __name__ == '__main__':
  main()
