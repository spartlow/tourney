import tourney
import history

t = tourney.Tourney()
games_string = '''
Steve Dave Jim over Brian Gene Shannon
  Shannon Sam Seth over Steve Brian Jim
Dave Gene Seth over Brian Jennn
'''
#t.parse_games(games_string)
#df = tourney.get_scores_per_game_dataframe(t, tourney.ELO)
#print(df.head(3))

all_games = ""

for key in history.history:
    print(key+" ELO:")
    all_games += "\n" + history.history[key]
    t = tourney.Tourney()
    t.parse_games(history.history[key])
    df = tourney.get_scores_per_game_dataframe(t, tourney.ELO)
    print(df)
    #print(df.drop(columns="Game Summaries").iloc[-1])
    print(df.drop(columns="Game Summaries").iloc[-1].sort_values())

t_all = tourney.Tourney()
t_all.parse_games(all_games)
df = tourney.get_scores_per_game_dataframe(t_all, tourney.ELO)
print("All Time ELO:")
print(df.drop(columns="Game Summaries").iloc[-1].sort_values())

