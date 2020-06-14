'''
Scoring systems for Tourney
'''
import random
import pandas

class ScoringSystem:
    "A virtual class for scoring systems"
    def __init__(self, tourney):
        self.tourney = tourney
    def get_player_scores(self):
        "Get dict of player names to thier score."
        scores = {}
        for name in self.tourney.get_player_names():
            scores[name] = self.get_player_score(name)
        return scores
    def get_player_scores_series(self):
        return pandas.Series(self.get_player_scores()).sort_values()
    def get_player_score(self, name):
        "Return the score of a single player by name. A higher score is considered better."
        return None


class RandomScorer(ScoringSystem):
    "A terrible, example scoring system where everyone gets a random score each time"
    def get_player_score(self, name):
        return random.random()

class WinPercentageScorer(ScoringSystem):
    "Score based solely on win percentage"
    def get_player_score(self, name):
        return self.tourney.get_win_pct(name)


class ELO(ScoringSystem):
    "Scoring system based on ELO used in chess and other tournaments"
    # http://www.lifewithalacrity.com/2006/01/ranking_systems.html

    def __init__(self, tourney):
        self.tourney = tourney
        self.starting_score = 1500
        self.max_score_loss = 32 #* 5
        self._build_scores()

    def get_player_score(self, name):
        if name not in self.player_scores:
            self.player_scores[name] = self.starting_score
        return self.player_scores[name]

    def _get_game_expectation(self, team_a, team_b):
        ''' Return expectation that Team A wins over Team B'''
        r_a = 0
        for name in team_a:
            r_a += self.get_player_score(name)
        r_b = 0
        for name in team_b:
            r_b += self.get_player_score(name)
        e_a = 1 / ( 1 + 10 ** ( (r_b - r_a) / 400 ) )
        return e_a
        
    def _score_game(self, game):
        e_a = self._get_game_expectation(game['winners'],game['losers'])
        score_exchange = (self.max_score_loss * len(game['losers'])) * (1 - e_a)
        winner_win = score_exchange / len(game['winners'])
        loser_loss = score_exchange / len(game['losers'])
        for name in game['winners']:
            self.player_scores[name] += winner_win
        for name in game['losers']:
            self.player_scores[name] -= loser_loss

    def _build_scores(self):
        self.player_scores = {k:self.starting_score for k in self.tourney.get_player_names()}
        for game in self.tourney.get_games():
            self._score_game(game)

class WinBonusScorer(ScoringSystem):
    """Score is win percentage plus bonuses for hard games
    
    Additionally, each score is record is padded up to 5 games with losses.
    """
    def __init__(self, tourney):
        self.tourney = tourney
        self.min_games = 5
        self.bonus_factor = 1 #0.5
        self._build_game_bonuses()

    def get_player_score(self, name):
        score = self.get_adjusted_win_pct(name) + (self.get_player_bonuses(name) \
            * self.bonus_factor) / \
            max(5,self.tourney.get_win_count(name) + self.tourney.get_loss_count(name)) * 100
        return score

    def get_adjusted_win_pct(self, name):
        wins = self.tourney.get_win_count(name)
        losses = self.tourney.get_loss_count(name)
        games = max(self.min_games,wins+losses)
        return wins / games

    def get_player_bonuses(self,name):
        return self.bonuses_df[name].sum()
    
    def _build_game_bonuses(self):
        self.bonuses_df = self.tourney.get_dataframe().copy()
        for col in self.bonuses_df.columns:
            self.bonuses_df[col].values[:] = 0
        game_number = 0
        for game in self.tourney.get_games():
            winners_power = 0
            losers_power = 0
            for winner in game['winners']:
                winners_power += self.get_adjusted_win_pct(winner)
            for loser in game['losers']:
                losers_power += self.get_adjusted_win_pct(loser)
            for winner in game['winners']:
                my_power = self.get_adjusted_win_pct(winner)
                bonus = max(0,losers_power - winners_power + my_power)
                self.bonuses_df[winner][game_number] = bonus
            game_number += 1

            



