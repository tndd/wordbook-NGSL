from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from db_command import (
  select_unanswered,
  select_versions,
  select_all,
  insert_test_result,
  insert_new_version,
  insert_child_version
)

# enums
class TestCategory(Enum):
  NGLS = 'ngsl'
  NAWL = 'nawl'
  TSL = 'tsl'
  BSL = 'bsl'

class ResponseStatus(Enum):
  UNANSERED = None
  CORRECT = 1
  WRONG = 0

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
  response_status: ResponseStatus

  def is_correct(self):
    return self.response_status == ResponseStatus.CORRECT

  def is_wrong(self):
    return self.response_status == ResponseStatus.WRONG

  def is_unanswered(self):
    return self.response_status == ResponseStatus.UNANSERED

@dataclass
class Version:
  id: str
  parent_id: Optional[str]
  name: str
  category: TestCategory
  remains: int
  timestamp: str

  def is_complete(self):
    return self.remains == 0
  
  def is_root(self):
    return self.parent_id == None

# repository
@dataclass
class WordRepository:
  version: Version

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
      meaning_in_english=row[7],
      response_status=ResponseStatus(row[8])
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
    if self.version.is_root():
      # child
      word_rows = select_all(self.version.id, self.version.category.value)
    else:
      # origin
      word_rows = select_all(self.version.parent_id, self.version.category.value)
    return self.rows_to_models(word_rows)
  
  def get_words_correct(self) -> List[Word]:
    words = self.get_words()
    return list(filter(lambda w: w.is_correct(), words))

  def get_words_wrong(self) -> List[Word]:
    words = self.get_words()
    return list(filter(lambda w: w.is_wrong(), words))

  def get_words_unanswered(self) -> List[Word]:
    words = self.get_words()
    return list(filter(lambda w: w.is_unanswered(), words))
  
  def regist_test_result(self, word: Word, is_collect: bool) -> None:
    if is_collect:
      insert_test_result(self.version.id, word.id, 1)
    else:
      insert_test_result(self.version.id, word.id, 0)

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
  
  @classmethod
  def create_child_version(cls, version: Version, name: str) -> Version:
    version_id = insert_child_version(version.id, name)
    return cls.get_by_id(version_id)
  
if __name__ == "__main__":
  vr = VersionReository()
  v = vr.get_by_id('eebed305-04f0-4671-8dd6-598abac53029')
  wr = WordRepository(v)
  print(len(wr.get_words_correct()))
  print(len(wr.get_words_wrong()))
  print(len(wr.get_words_unanswered()))
  # print(wr.get_words()[0])
  # words = wr.get_unanswered_words()
  # print(words[0])
  # word = wr.get_words()[0]
  # print(len(wr.get_words()))
  # wr.regist_test_result(word, True)
  # wr = WordRepository.create_new_version('v0', TestCategory.NGLS)
  # print(wr.version_id)
  # print(vr.create_child_version(v, 'tsttst'))
  # print(v)
  # print(v.is_child())
  # v = vr.create_version('test_test', TestCategory.NAWL)
  # print(v)
  # vs = vr.get_versions()
  # print(vs)
  # print(vr.get_by_id('b23ad014-84b9-45fa-94be-0dc4035a6d60'))
