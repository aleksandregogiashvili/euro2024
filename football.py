import requests
import sqlite3


api_url = 'https://api.football-data.org/v2/competitions/EC/matches'
headers = {'X-Auth-Token': 'f5321dab4ab34d4c86f64d3d0aab7297'}


response = requests.get(api_url, headers=headers)
data = response.json()


conn = sqlite3.connect('football_matches.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    home_team TEXT,
    away_team TEXT,
    home_score INTEGER,
    away_score INTEGER,
    match_date TEXT
)
''')


for match in data['matches']:
    cursor.execute('''
    INSERT INTO matches (match_id, home_team, away_team, home_score, away_score, match_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (match['id'], match['homeTeam']['name'], match['awayTeam']['name'],
          match['score']['fullTime']['homeTeam'], match['score']['fullTime']['awayTeam'],
          match['utcDate']))


conn.commit()
conn.close()