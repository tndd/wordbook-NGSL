-- get a list of incorrect or unanswered words.
-- args: [class, version, type]
select w.id, w.word, w.translation, w.explanation, w.example, w.example_translation, w.pronunciation, w.meaning_in_english 
from word w
left join (select * from test where version=? and version=?) t
on (w.id=t.word_id)
where "type"=? and (t.correct=0 or t.correct is NULL);