from dataclasses import dataclass

from db_command import select_incorrect, select_unanswered

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
  category: str

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

  def get_unanswered_words(self):
    word_rows = select_unanswered(self.version_id, self.category)
    return self.rows_to_models(word_rows)

  def get_incorrect_words(self):
    print(self.version_id, self.category)
    word_rows = select_incorrect(self.version_id, self.category)
    return self.rows_to_models(word_rows)


if __name__ == "__main__":
  wr = WordRepository('6027924c-419f-40ae-8b83-454dfa6cd21a', 'ngsl')
  words = wr.get_unanswered_words()
  print(words[1])