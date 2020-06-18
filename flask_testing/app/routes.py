from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/scores')
def scores():
    players = [
        {
            'rank': 1,
            'name': 'Dave',
            'wins': 5,
            'losses': 0,
            'adj_score': 20
        },
        {
            'rank': 2,
            'name': 'Steve',
            'wins': 3,
            'losses': 2,
            'adj_score': 10
        },
        {
            'rank': 3,
            'name': 'Sam',
            'wins': 1,
            'losses': 4,
            'adj_score': 4
        }
    ]
    return render_template('scores.html', title='Scores', players=players)

@app.route('/stats')
def stats():
    return render_template('stats.html', title='Stats')