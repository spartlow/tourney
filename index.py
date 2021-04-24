from flask import Flask, render_template
import tourney
import scoring
import history
import pandas


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
