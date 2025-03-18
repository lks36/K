CREATE TABLE question_debat(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_thematique INTEGER,
    q1 TEXT,
    q2 TEXT,
    q3 TEXT,
    q4 TEXT,
    q5 TEXT,
    q6 TEXT,
    q7 TEXT,
    q8 TEXT,
    q9 TEXT,
    q10 TEXT,
    FOREIGN KEY (id_thematique) REFERENCES thematique(id)
)
