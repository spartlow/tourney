import tourney
import scoring
import history
import pandas

games_string = '''
Steve Dave Jim over Brian Gene Shannon
  Shannon Sam Seth over Steve Brian Jim
Dave Gene Seth over Brian Jennn
Jennn over Gene Seth Jim
'''

#t = tourney.Tourney()
#t.parse_games(games_string)
#print(t.get_possible_games(3))


#t = tourney.Tourney()
#t.parse_games(games_string)
#df = tourney.get_scores_per_game_dataframe(t, scoring.ELO)
#print(df.head(3))

#"""
all_games = history.get_all_games()

#for key in history.history:
    #if key not in ['T12', 'T13']:
        #all_games += "\n" + history.history[key]
    #print(key+" WinBonusScorer:")
    #t = tourney.Tourney()
    #t.parse_games(history.history[key])
    #df = tourney.get_scores_per_game_dataframe(t, scoring.WinBonusScorer)
    #print(df)
    #print(df.drop(columns="Game Summaries").iloc[-1].sort_values())

t_all = tourney.Tourney()
t_all.parse_games(all_games)

df = tourney.get_scores_per_game_dataframe(t_all, scoring.ELO)
print("All Time ELO:")
print(df.drop(columns="Game Summaries").iloc[-1].sort_values())


df = tourney.get_scores_per_game_dataframe(t_all, scoring.WinBonusScorer)
print("All Time WinBonus:")
print(df.drop(columns="Game Summaries").iloc[-1].sort_values())



#t_all.parse_games(all_games)
scores = scoring.WinPercentageScorer(t_all).get_player_scores_series()
print("\nAll Time Win Percentage:")
print(scores)

print("\nAll Time Stats:")
print(t_all.get_all_player_stats_dataframe().sort_values("games"))

print("\nPVP:")
print(t_all.get_pvp_win_df())
#print(t_all.get_pvp_win_df()[t_all.get_pvp_win_df().index.isin(['Steve'], level=0)])

print("\nFairest games:")
#t = tourney.Tourney()
#t.parse_games(history.tournament16)
print(scoring.WinPercentageScorer(t_all).get_fairest_games(2, players=['Steve', 'Brian', 'Jim', 'Dave', 'Sam']))

#print(t_all.get_possible_teams(5))
print("\nUnplayed teams:")
print(t_all.get_unplayed_teams(3, players=['Steve', 'Brian', 'Jim', 'Dave', 'Sam']))

#print("\nT15:")
#t = tourney.Tourney()
#t.parse_games(history.history["T15"])
#scores = scoring.WinPercentageScorer(t).get_player_scores_series()
#print("\nT15 Win Percentage:")
#print(scores)
#scorer = scoring.WinBonusScorer(t)
#print(scorer.bonuses_df)
#print(scorer.get_player_scores())
#"""
