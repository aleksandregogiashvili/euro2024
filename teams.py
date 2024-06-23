import sqlite3


conn = sqlite3.connect('euros.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    match TEXT NOT NULL,
    result TEXT NOT NULL
)
''')
matches = [
    ('2024-06-14', 'Germany vs Scotland', '5-1'),
    ('2024-06-15', 'Hungary vs Switzerland', '1-3'),
    ('2024-06-15', 'Spain vs Croatia', '3-0'),
    ('2024-06-15', 'Italy vs Albania', '2-1'),
    ('2024-06-16', 'Poland vs Netherlands', '1-2'),
    ('2024-06-16', 'Slovenia vs Denmark', '1-1'),
    ('2024-06-16', 'Serbia vs England', '0-1'),
    ('2024-06-17', 'Romania vs Ukraine', '3-0'),
    ('2024-06-17', 'Belgium vs Slovakia', '0-1'),
    ('2024-06-17', 'Austria vs France', '0-1'),
    ('2024-06-18', 'Turkiye vs Georgia', '3-1'),
    ('2024-06-19', 'Croatia vs Albania', '2-2'),
    ('2024-06-19', 'Germany vs Hungary', '2-0'),
    ('2024-06-19', 'Scotland vs Switzerland', '1-1'),
    ('2024-06-20', 'Slovenia vs Serbia', '1-1'),
    ('2024-06-20', 'Denmark vs England', '1-1'),
    ('2024-06-21', 'Slovakia vs Ukraine', '1-2'),
    ('2024-06-21', 'Poland vs Austria', '1-3'),
    ('2024-06-21', 'Netherlands vs France', '0-0'),
]

c.executemany('''
INSERT INTO Matches (date, match, result)
VALUES (?, ?, ?)
''', matches)



conn.commit()
conn.close()
