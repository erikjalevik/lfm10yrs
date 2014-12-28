import sys, csv, datetime, sqlite3

# 0 "ISO time"
# 1 "unixtime"
# 2 "track name"
# 3 "track mbid"
# 4 "artist name"
# 5 "artist mbid"
# 6 "uncorrected track name"
# 7 "uncorrected track mbid"
# 8 "uncorrected artist name"
# 9 "uncorrected artist mbid"

def main():

  args = sys.argv[1:]
  if not args:
      print("Usage: %s filename dbfile" % sys.argv[0])
      return

  scrobbleFilename = args[0]
  dbFilename = args[1]
  
  file = open(scrobbleFilename, "r", encoding="utf8")
  reader = csv.reader(file, delimiter="\t")
  next(reader) # skip header row

  conn = sqlite3.connect(dbFilename)
  c = conn.cursor()

  for line in reader:
    unixtime = int(line[1])
    track = line[2]
    trackMbid = line[3]
    artist = line[4]
    artistMbid = line[5]

    # Artist table
    c.execute("INSERT OR IGNORE INTO artist (name, mbid) VALUES (?, ?)", (artist, artistMbid))
    
    # Track table
    c.execute("SELECT id FROM artist WHERE name=?", (artist,))
    artistId = c.fetchone()[0]
    c.execute("INSERT OR IGNORE INTO track (title, mbid, artist_id) VALUES (?, ?, ?)", (track, trackMbid, artistId))

    # Scrobble table
    c.execute("SELECT id FROM track WHERE title=? AND artist_id=?", (track, artistId))
    trackId = c.fetchone()[0]
    c.execute("INSERT INTO scrobble (track_id, timestamp) VALUES (?, ?)", (trackId, unixtime))

  conn.commit()
  conn.close()
  
    
if __name__ == '__main__':
  main()

    
    
    
    
    
    
      #london = datetime.timedelta(hours = +0);
      #berlin = datetime.timedelta(hours = +1);
      #dt = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(london))
      
      #dateString = "{0}/{1}/{2} {3:02d}:{4:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
      #titleString = "{0} - {1}".format(line[4], line[2]) #.encode("ascii", "ignore")
