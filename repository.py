from dataclasses import dataclass

from db_command import select_unanswered

# datamodels
@dataclass
class Word:
  id: int
  word: str
  translation: str
  explanation: str
  example: str
  example_translation: str
  pronunciation: str
  meaning_in_english: str

# util methods
def row_to_model(row):
  return Word(
    id=row[0],
    word=row[1],
    translation=row[2],
    explanation=row[3],
    example=row[4],
    example_translation=row[5],
    pronunciation=row[6],
    meaning_in_english=row[7]
  )

def rows_to_models(rows):
  models = []
  for r in rows:
    models.append(row_to_model(r))
  return models

# repository
def get_unanswered_words(version_id, type_):
  word_rows = select_unanswered(version_id, type_)
  return rows_to_models(word_rows)


if __name__ == "__main__":
  words = get_unanswered_words('6027924c-419f-40ae-8b83-454dfa6cd21a', 'ngsl')
  print(words[0])