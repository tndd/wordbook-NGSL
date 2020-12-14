CREATE TABLE test (
  version_id TEXT NOT NULL,
  word_id INTEGER NOT NULL,
  "timestamp" TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
  correct INTEGER NOT NULL,
  PRIMARY KEY(version_id, word_id),
  foreign key(word_id) references word(id)
);