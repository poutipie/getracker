
CREATE TABLE IF NOT EXISTS Item (
  [id]          INTEGER PRIMARY KEY    NOT NULL,

  [name]        TEXT                   NOT NULL,
  [examine]     TEXT                   NOT NULL,
  [value]       INTEGER                NOT NULL,
  [icon]        TEXT                   NOT NULL,
  [ge_limit]    INTEGER                NOT NULL,
  [members]     BOOLEAN                NOT NULL,
  [low_alch]    INTEGER                NOT NULL,
  [high_alch]   INTEGER                NOT NULL
);

CREATE TABLE IF NOT EXISTS ItemIndexTime (
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [indexed_at]  DATE                   NOT NULL
);

CREATE TABLE IF NOT EXISTS Volume (
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [volume]      INTEGER                NOT NULL,
  [item_id]     INTEGER                NOT NULL,

  FOREIGN KEY(item_id)  REFERENCES Item(id)
);

CREATE TABLE IF NOT EXISTS VolumeIndexTime(
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [indexed_at]  DATE                   NOT NULL
);

CREATE TABLE IF NOT EXISTS Price (
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [high]        INTEGER,
  [high_time]    DATE,
  [low]         INTEGER,
  [low_time]     DATE,
  [item_id]     INTEGER                NOT NULL,

  FOREIGN KEY(item_id)  REFERENCES Item(id)
);

CREATE TABLE IF NOT EXISTS PriceIndexTime (
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [indexed_at]  DATE                   NOT NULL
);
