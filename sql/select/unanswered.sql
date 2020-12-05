select w.id, w.word, w.translation, w.explanation, w.example, w.example_translation, w.pronunciation, w.meaning_in_english
from word w
left join (select * from test where version_id=?) t
on w.id=t.word_id
where "category"=? and t.correct is NULL;