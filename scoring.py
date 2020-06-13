'''
Scoring systems for Tourney
'''
import random

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
    def get_player_score(self, name):
        "Return the score of a single player by name. A higher score is considered better."
        return None


class RandomScorer(ScoringSystem):
    "A terrible, example scoring system where everyone gets a random score each time"
    def get_player_score(self, name):
        return random.random()

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
    ''' Return expectation that Team A wins over Team B'''
    def _get_game_expectation(self, team_a, team_b):
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