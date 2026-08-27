CREATE TABLE IF NOT EXISTS sticky (
  id SERIAL PRIMARY KEY,
  channel BIGINT NOT NULL,
  title TEXT NOT NULL,
  enabled BOOLEAN NOT NULL,
  msg TEXT NOT NULL,
  trigger_msgs INTEGER NOT NULL,
  trigger_minutes INTEGER NOT NULL
);