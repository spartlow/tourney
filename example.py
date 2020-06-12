import tourney
t = tourney.Tourney()
games_string = '''
... Steve Dave Jim over Brian Gene Shannon
...  Shannon Sam Seth over Steve Brian Jim
... Dave Gene Seth over Brian Jennn
... '''
t.parse_games(games_string)
df = tourney.get_scores_per_game_dataframe(t, tourney.ELO)
print(df.head(3))