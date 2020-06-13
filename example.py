import tourney
import tournaments

t = tourney.Tourney()
games_string = '''
Steve Dave Jim over Brian Gene Shannon
  Shannon Sam Seth over Steve Brian Jim
Dave Gene Seth over Brian Jennn
'''
t.parse_games(games_string)
df = tourney.get_scores_per_game_dataframe(t, tourney.ELO)
print(df.head(3))

for key in tournaments.tournaments:
    print(key+":")
    t = tourney.Tourney()
    t.parse_games(tournaments.tournaments[key])
    df = tourney.get_scores_per_game_dataframe(t, tourney.ELO)
    print(df)
    #print(df.drop(columns="Game Summaries").iloc[-1])
    print(df.drop(columns="Game Summaries").iloc[-1].sort_values())
