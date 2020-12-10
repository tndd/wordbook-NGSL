from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import uuid

from db_command import (
  select_incorrect,
  select_unanswered,
  select_parent_version,
  select_versions,
  insert_test_result,
  insert_new_version
)

# enums
class TestCategory(Enum):
  NGLS = 'ngsl'
  NAWL = 'nawl'
  TSL = 'tsl'
  BSL = 'bsl'

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

@dataclass
class Version:
  id: str
  parent_id: str
  name: str
  category: TestCategory
  remains: int
  timestamp: str

  def is_complete(self):
    return self.remains == 0

# repository
@dataclass
class WordRepository:
  version_id: str

  @staticmethod
  def row_to_model(row: list) -> Word:
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
  def rows_to_models(cls, rows: List[list]) -> List[Word]:
    models = []
    for r in rows:
      models.append(cls.row_to_model(r))
    return models
  
  @classmethod
  def create_new_version(cls, name: str, category: TestCategory) -> 'WordRepository':
    version_id = insert_new_version(name, category.value)
    return cls(version_id)
  
  def get_words(self) -> List[Word]:
    parent_version_id = select_parent_version(self.version_id)
    word_rows = []
    if parent_version_id:
      # child
      word_rows = select_incorrect(parent_version_id)
    else:
      # origin
      word_rows = select_unanswered(self.version_id)
    return self.rows_to_models(word_rows)
  
  def regist_test_result(self, word: Word, is_collect: bool) -> None:
    if is_collect:
      insert_test_result(self.version_id, word.id, 1)
    else:
      insert_test_result(self.version_id, word.id, 0)

@dataclass
class VersionReository:
  @staticmethod
  def row_to_model(row: list) -> Version:
    v_id = row[0]
    return Version(
      id=v_id,
      parent_id=row[1],
      name=row[2],
      category=TestCategory(row[3]),
      timestamp=row[4],
      remains=len(select_unanswered(v_id))
    )
  
  @classmethod
  def rows_to_models(cls, rows: List[list]) -> List[Version]:
    models = []
    for r in rows:
      models.append(cls.row_to_model(r))
    return models

  @classmethod
  def get_versions(cls) -> List[Version]:
    version_rows = select_versions()
    return cls.rows_to_models(version_rows)

  @classmethod
  def get_by_id(cls, version_id: str) -> Version:
    versions = cls.get_versions()
    return next(filter(lambda v: v.id == version_id, versions))

  @classmethod
  def create_version(cls, name: str, category: TestCategory) -> Version:
    version_id = insert_new_version(name, category.value)
    return cls.get_by_id(version_id)

if __name__ == "__main__":
  # wr = WordRepository('6027924c-419f-40ae-8b83-454dfa6cd21a')
  # words = wr.get_unanswered_words()
  # print(words[0])
  # word = wr.get_words()[0]
  # print(len(wr.get_words()))
  # wr.regist_test_result(word, True)
  # wr = WordRepository.create_new_version('v0', TestCategory.NGLS)
  # print(wr.version_id)
  vr = VersionReository()
  v = vr.create_version('test_test', TestCategory.NAWL)
  print(v)
  # vs = vr.get_versions()
  # print(vs)
  # print(vr.get_by_id('b23ad014-84b9-45fa-94be-0dc4035a6d60'))
