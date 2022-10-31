-- 01
SELECT name FROM songs;

-- 02
SELECT name FROM songs ORDER BY tempo ASC;

-- 03
SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;

-- 04
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;

-- 05
SELECT AVG(energy) FROM songs;

-- 06
SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Post Malone");

-- 07
SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake");

-- 08
SELECT name FROM songs WHERE name LIKE "%feat.%";
