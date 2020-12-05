CREATE TABLE word(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  category TEXT NOT NULL,
  word TEXT NOT NULL,
  translation TEXT NOT NULL,
  explanation TEXT NOT NULL,
  example TEXT NOT NULL,
  example_translation TEXT NOT NULL,
  pronunciation TEXT NOT NULL,
  meaning_in_english TEXT
);