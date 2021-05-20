from flask import Flask, render_template, request
from cycler import cycler
import pandas
import re
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import tourney
import scoring
import history

app = Flask(__name__)

pandas.set_option('display.max_colwidth', -1)

@app.route('/')
def print_index():
    contents = '''
    '''
    return render_template('basic.html', heading="Index", contents=contents)

@app.route('/games')
def print_games():
    games = open("data/games.txt", "r").read()
    t = tourney.Tourney()
    t.parse_games(games)
    #return render_template('stats.html', list = t.get_games(), heading="Games")
    return render_template('games.html', games = t.get_games(), heading="Games2")

@app.route('/stats')
def print_stats():
    #plt.rc('axes', prop_cycle=(cycler('linestyle', ['-', '--', ':'])))
    games = open("data/games.txt", "r").read()
    t = tourney.Tourney()
    t.parse_games(games)
    #df = t.get_all_player_stats_dataframe().sort_values(by="games", ascending=False)
    df = tourney.get_scores_per_game_dataframe(t, scoring.WinBonusScorer)

    fig = plt.figure()
    ax = fig.subplots()
    df.plot(ax=ax)
    #ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    image = f"<img src='data:image/png;base64,{data}'/>"
    return render_template('scores.html', \
        tables=[ \
            t.get_all_player_stats_dataframe(scoring.WinBonusScorer).sort_values(by="games", ascending=False).to_html(), \
            scoring.WinBonusScorer(t).bonuses_df.to_html(), \
            df.to_html(classes='data')], \
        heading="Tournament Stats", image=image)

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

@app.route('/predict')
def print_prediction():
    team_a = "Seth Sam Dave"
    team_b = "Steve Brian"
    games = open("data/games.txt", "r").read()
    t = tourney.Tourney()
    t.parse_games(games)
    exp_a = scoring.WinBonusScorer(t).get_game_expectation(team_a.split(" "), team_b.split(" "))
    return str(exp_a)

@app.route('/build-team')
def print_build_team():
    players = "Steve Brian Dave Seth Sam"
    t = tourney.Tourney()
    t.parse_games(history.get_all_games())
    games = scoring.WinBonusScorer(t).get_fairest_games(players=players.split(" "))
    return render_template('basic.html', contents=games)



@app.route('/test')
def print_test():
    games = open("data/games.txt", "r").read()
    t = tourney.Tourney()
    t.parse_games(games)
    return render_template('game-summary.html', index=1, game=t.get_games()[0])
