from dataclasses import dataclass

from db_command import (
  select_incorrect,
  select_unanswered,
  select_parent_version
)

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

# repository
@dataclass
class WordRepository:
  version_id: str

  @staticmethod
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

  @classmethod
  def rows_to_models(cls, rows):
    models = []
    for r in rows:
      models.append(cls.row_to_model(r))
    return models
  
  def get_words(self):
    parent_version_id = select_parent_version(self.version_id)
    word_rows = []
    if parent_version_id:
      # child
      word_rows = select_incorrect(parent_version_id)
    else:
      # origin
      word_rows = select_unanswered(self.version_id)
    return self.rows_to_models(word_rows)


if __name__ == "__main__":
  wr = WordRepository('6027924c-419f-40ae-8b83-454dfa6cd21a')
  # words = wr.get_unanswered_words()
  # print(words[0])
  # print(wr.get_words()[0])
  print(len(wr.get_words()))