from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
# import sqlite3


app = Flask(__name__)
app.secret_key = 'asdadas'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///euros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    match = db.Column(db.String(200))
    result = db.Column(db.String(100))



teams = [
    {'name': 'Germany', 'logo': 'italy.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Italy_at_the_UEFA_European_Championship'},
    {'name': 'Spain', 'logo': 'spain.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Spain_at_the_UEFA_European_Championship'},
    {'name': 'Albania', 'logo': 'albania.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Albania_at_the_UEFA_European_Championship'},
    {'name': 'Austria', 'logo': 'austria.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Austria_at_the_UEFA_European_Championship'},
    {'name': 'Belgium', 'logo': 'belgium.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Belgium_at_the_UEFA_European_Championship'},
    {'name': 'Croatia', 'logo': 'croatia.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Croatia_at_the_UEFA_European_Championship'},
    {'name': 'Czechia', 'logo': 'czechia.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Czechia_at_the_UEFA_European_Championship'},
    {'name': 'Denmark', 'logo': 'denmark.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Denmark_at_the_UEFA_European_Championship'},
    {'name': 'England', 'logo': 'england.png', 'wiki_url': 'https://en.wikipedia.org/wiki/England_at_the_UEFA_European_Championship'},
    {'name': 'France', 'logo': 'france.png', 'wiki_url': 'https://en.wikipedia.org/wiki/France_at_the_UEFA_European_Championship'},
    {'name': 'Georgia', 'logo': 'georgia.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Georgia_at_the_UEFA_European_Championship'},
    {'name': 'Hungary', 'logo': 'hungary.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Hungary_at_the_UEFA_European_Championship'},
    {'name': 'Italy', 'logo': 'italy.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Italy_at_the_UEFA_European_Championship'},
    {'name': 'Netherlands', 'logo': 'netherlands.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Netherlands_at_the_UEFA_European_Championship'},
    {'name': 'Poland', 'logo': 'poland.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Poland_at_the_UEFA_European_Championship'},
    {'name': 'Portugal', 'logo': 'portugal.jpg', 'wiki_url': 'https://en.wikipedia.org/wiki/Portugal_at_the_UEFA_European_Championship'},
    {'name': 'Romania', 'logo': 'romania.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Romania_at_the_UEFA_European_Championship'},
    {'name': 'Scotland', 'logo': 'scotland.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Scotland_at_the_UEFA_European_Championship'},
    {'name': 'Serbia', 'logo': 'serbia.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Serbia_at_the_UEFA_European_Championship'},
    {'name': 'Slovakia', 'logo': 'slovakia.jpg', 'wiki_url': 'https://en.wikipedia.org/wiki/Slovakia_at_the_UEFA_European_Championship'},
    {'name': 'Slovenia', 'logo': 'slovenia.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Slovenia_at_the_UEFA_European_Championship'},
    {'name': 'Switzerland', 'logo': 'switzerland.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Switzerland_at_the_UEFA_European_Championship'},
    {'name': 'Turkiye', 'logo': 'turkiye.png', 'wiki_url': 'https://en.wikipedia.org/wiki/Turkiye_at_the_UEFA_European_Championship'},
    {'name': 'Ukraine', 'logo': 'ukraine.jpg', 'wiki_url': 'https://en.wikipedia.org/wiki/Ukraine_at_the_UEFA_European_Championship'}

]


# def get_matches():
#     conn = sqlite3.connect('euros.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM matches")
#     matches = c.fetchall()
#     conn.close()
#     return matches
# def get_matches():
#     conn = sqlite3.connect('euros.db')
#     c = conn.cursor()
#     c.execute('SELECT date, match, result FROM matches')
#     matches = c.fetchall()
#     conn.close()
#     return matches


users = {
    'user1': {'password': 'password1', 'email': 'user1@example.com'},
    'user2': {'password': 'password2', 'email': 'user2@example.com'}
}



@app.route('/football-api')
def football_api():
    url = "https://api.football-data.org/v2/competitions/EC/matches"

    headers = {
        'X-Auth-Token': 'f5321dab4ab34d4c86f64d3d0aab7297'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matches_data = response.json().get('matches', [])


        Match.query.delete()


        for match in matches_data:
            date = match['utcDate']
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            score = f"{match['score']['fullTime']['homeTeam']} - {match['score']['fullTime']['awayTeam']}"

            new_match = Match(date=date, match=f"{home_team} vs {away_team}", result=score)
            db.session.add(new_match)

        db.session.commit()

        flash('Football API data updated successfully.', 'success')
    else:
        flash('Failed to fetch football API data.', 'error')


    matches = Match.query.all()

    return render_template('football_api.html', matches=matches)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        if username_or_email in users:
            if password == users[username_or_email]['password']:
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('Username/Email not found. Please register if you are a new user.', 'error')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        users[username] = {'password': password, 'email': email}

        flash('Registration successful!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')



@app.route('/teams')
def teams_page():
    return render_template('teams.html', teams=teams)

@app.route('/match-results')
def get_matches():
    matches = Match.query.all()
    return render_template('matches.html', matches=matches)



# @app.route('/match-results')
# def match_results():
#     matches = get_matches()
#     return render_template('matches.html', matches=matches)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        with app.app_context():
            db.create_all()

    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

