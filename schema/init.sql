CREATE TABLE IF NOT EXISTS levels (
  id BIGINT PRIMARY KEY,
  xp INTEGER,
  lvl INTEGER
);
CREATE TABLE IF NOT EXISTS options (
  beep TEXT DEFAULT 'boop',
  doublexp BOOLEAN DEFAULT FALSE,
  eventmode BOOLEAN DEFAULT FALSE,
  eventroleid BIGINT DEFAULT 0 
);
INSERT INTO options default values;