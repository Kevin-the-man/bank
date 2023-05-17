-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  username  TEXT    UNIQUE NOT NULL,
  password  TEXT    NOT NULL,
  firstname  TEXT    NOT NULL,
  lastname  TEXT    NOT NULL,
  balance   NUMERIC(10,2)   DEFAULT 0   NOT NULL
);

insert into user (username,password, firstname, lastname, balance) VALUES ('admin','admin', 'admin', 'admin', 10000);
