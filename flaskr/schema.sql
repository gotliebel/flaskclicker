DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  money INTEGER,
  cost_upgrade_click INTEGER,
  cost_upgrade_autoclicker INTEGER,
  coins_per_click INTEGER,
  coins_per_sec INTEGER,
  last_time INTEGER
);
