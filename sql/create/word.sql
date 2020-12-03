CREATE TABLE word(
  id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
  type STRING NOT NULL,
  word STRING NOT NULL,
  translation STRING NOT NULL,
  explanation STRING NOT NULL,
  example STRING NOT NULL,
  example_translation STRING NOT NULL,
  pronunciation STRING NOT NULL,
  meaning_in_english STRING
);