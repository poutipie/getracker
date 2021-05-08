
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

CREATE TABLE IF NOT EXISTS ItemIndexMeta (
  [id]          INTEGER PRIMARY KEY    AUTOINCREMENT,

  [updated_in]  DATE                   NOT NULL
);