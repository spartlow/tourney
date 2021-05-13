from flask import Flask, render_template, request
import tourney
import scoring
import history
import pandas
import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    contents = '''
    <a href="stats">Stats</a><br><br>
    <a href="stats2">Stats2</a><br><br>
    <a href="add-game">Add a game</a><br><br>
    '''
    return render_template('basic.html', heading="Index", contents=contents)

@app.route('/stats')
def print_stats():
    t_all = tourney.Tourney()
    t_all.parse_games(history.get_all_games())
    df = t_all.get_all_player_stats_dataframe().sort_values(by="games", ascending=False)
    return render_template('stats.html', tables=[df.to_html(classes='data')], heading="All time stats")

@app.route('/stats2')
def print_stats2():
    t_all = tourney.Tourney()
    t_all.parse_games(history.get_all_games())
    df = t_all.get_pvp_win_df()
    return render_template('stats.html', tables=[df.to_html(classes='data')], heading="All time stats")

@app.route('/add-game', methods=['GET', 'POST'])
def print_addgame():
    if request.method == 'POST':
        game_summary = request.form['input-game-summary'].strip()
        print(game_summary)
        if re.match(r"^([\w]+ )+OVER( [\w]+)+$", game_summary):
            file1 = open("data/games.txt", "a")  # append mode
            file1.write(game_summary+"\n")
            file1.close()
            message = "Added game: "+game_summary+"."
        else:
            message = "Invalid input"

    else:
        message = ""
    f = open("data/players.txt", "r")
    players = f.read().splitlines()
    players.sort()
    #print(players)
    return render_template('add-game.html', players=players, heading="Add a game", message=message)
