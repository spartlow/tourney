import tourney
import scoring
import history

games_string = '''
Steve Dave Jim over Brian Gene Shannon
  Shannon Sam Seth over Steve Brian Jim
Dave Gene Seth over Brian Jennn
Jennn over Gene Seth Jim
'''
#t = tourney.Tourney()
#t.parse_games(games_string)
#df = tourney.get_scores_per_game_dataframe(t, scoring.ELO)
#print(df.head(3))
"""
all_games = ""

for key in history.history:
    print(key+" WinBonusScorer:")
    all_games += "\n" + history.history[key]
    t = tourney.Tourney()
    t.parse_games(history.history[key])
    df = tourney.get_scores_per_game_dataframe(t, scoring.WinBonusScorer)
    print(df)
    #print(df.drop(columns="Game Summaries").iloc[-1])
    print(df.drop(columns="Game Summaries").iloc[-1].sort_values())

t_all = tourney.Tourney()
t_all.parse_games(all_games)
df = tourney.get_scores_per_game_dataframe(t_all, scoring.ELO)
print("All Time ELO:")
print(df.drop(columns="Game Summaries").iloc[-1].sort_values())


#t_all.parse_games(all_games)
scores = scoring.WinPercentageScorer(t_all).get_player_scores_series()
print("\nAll Time Win Percentage:")
print(scores)

print("\nPVP:")
print(t_all.get_pvp_win_df())
"""

print("\nT15:")
t = tourney.Tourney()
t.parse_games(history.history["T15"])

#t_all.parse_games(all_games)
scores = scoring.WinPercentageScorer(t).get_player_scores_series()
print("\nT15 Win Percentage:")
print(scores)


#print("Steve wins: "+str(t.get_win_count("Steve")))
#print("Steve pct: "+str(t.get_win_pct("Steve")))
scorer = scoring.WinBonusScorer(t)
#scorer._build_game_bonuses()
print(scorer.bonuses_df)
print(scorer.get_player_scores())
