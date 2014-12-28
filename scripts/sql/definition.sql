DROP TABLE artist;
DROP TABLE track;
DROP TABLE scrobble;
DROP TABLE tag;
DROP TABLE artist_tag;
DROP TABLE track_tag;

CREATE TABLE artist (
  id         INTEGER PRIMARY KEY,
  name       VARCHAR UNIQUE NOT NULL,
  mbid       VARCHAR,
  listeners  INTEGER,
  plays      INTEGER,
  myrank     INTEGER
);

CREATE TABLE track (
  id        INTEGER PRIMARY KEY,
  title     VARCHAR NOT NULL,
  artist_id INTEGER NOT NULL,
  mbid      VARCHAR,
  duration  INTEGER,
  listeners INTEGER,
  plays     INTEGER,
  myrank    INTEGER
);

CREATE UNIQUE INDEX idx_titleArtist ON track(title, artist_id);

CREATE TABLE scrobble (
  id        INTEGER PRIMARY KEY,
  track_id  INTEGER NOT NULL,
  timestamp INTEGER NOT NULL
);

CREATE TABLE tag (
  id        INTEGER PRIMARY KEY,
  name      VARCHAR UNIQUE NOT NULL,
  reach     INTEGER,
  count     INTEGER
);

CREATE TABLE artist_tag (
  id        INTEGER PRIMARY KEY,
  artist_id INTEGER NOT NULL,
  tag_id    INTEGER NOT NULL,
  count     INTEGER
);

CREATE UNIQUE INDEX idx_artistTag ON artist_tag(artist_id, tag_id);

-- top tags included in track.getInfo
CREATE TABLE track_tag (
  id        INTEGER PRIMARY KEY,
  track_id  INTEGER NOT NULL,
  tag_id    INTEGER NOT NULL,
  count     INTEGER
);

CREATE UNIQUE INDEX idx_trackTag ON track_tag(track_id, tag_id);
