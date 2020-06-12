import re
import json
import pandas
import statistics

def parse_games(string):
    games = []
    lines = string.split("\n")
    #print(lines)
    pattern = re.compile(r"^([\s]*(?P<winner>[\w]+)[\s]*,?)+ (over|beat) ([\s]*(?P<loser>[\w]+)[\s]*,?)+( on (?P<time>.*))?$")
    for line in lines:
        if line.strip()=='':
            pass
        else:
            #matches = re.match(r"(?P<winners>.*) over (?P<losers>.*)( on (?P<time>.*))?",line)
            matches = re.match(r"(?P<winners>.*) over (?P<losers>.*)",line)
            #print(matches)
            #matches = re.findall(pattern,line)
            if not matches:
                print("Can't parse line: "+line)
                pass
            else:
                game = {}
                #print(matches)
                #print(matches.groups())
                #print(matches.group(1))
                #print(matches.group(2))
                teams = matches.groupdict()
                game['winners'] = teams['winners'].split()
                game['losers']  = teams['losers'].split()
                if ('time' in teams and teams['time']):
                    game['time']  = teams['time']
                games.append(game)
    #print(games)
    return(games)

def add_to_dataframe(df, name, row, value):
    if name not in df:
        df[name] = ""
    if len(df.index)<=row:
        df.loc[row] = ""
    df[name][row] = value;
def to_dataframe(games):
    df = pandas.DataFrame()
    for game in games:
        game_number = len(df.index)
        #if len(df.index):
        #    df.loc[game_number] = None
        for player in game['winners']:
            add_to_dataframe(df, player, game_number, "W")
        for player in game['losers']:
            add_to_dataframe(df, player, game_number, "L")
    return df

def get_adjusted_win_percentage(df, name):
    if name not in df:
        raise Exception("Unknown person: "+name)
    counts = df[name].value_counts()
    if 'W' in counts:
        wins = counts['W']
    else:
        wins = 0
    if 'L' in counts:
        losses = counts['L']
    else:
        losses = 0
    if wins+losses < 5: # magic number!
        losses = 5 - wins
    if wins==0:
        pct = 0.0
    else:
        pct = wins / (wins+losses)
    return pct

def get_raw_win_percentage(df, name):
    if name not in df:
        raise Exception("Unknown person: "+name)
    counts = df[name].value_counts()
    if 'W' in counts:
        wins = counts['W']
    else:
        wins = 0
    if 'L' in counts:
        losses = counts['L']
    else:
        losses = 0
    if wins==0:
        pct = 0.0
    else:
        pct = wins / (wins+losses)
    return pct

class Tourney:
    def __init__(self):
        self.games = None
        self.df = None
    def parse_games(self, str):
        games = parse_games(str)
        self.set_games(games)
    def set_games(self, games):
        self.games = games
        self.df = to_dataframe(games)
    def get_games(self):
        return self.games.copy()
    def get_game_summaries(self):
        summaries = []
        for game in self.games:
            summaries.append(', '.join(game['winners'])+' over '+', '.join(game['losers']))
        return summaries
    def get_dataframe(self):
        return self.dataframe
    def get_player_names(self):
        return list(self.df)
    def get_win_count(self, name):
        if name not in self.df:
            return None
        counts = df[name].value_counts()
        if 'W' in counts:
            return counts['W']
        else:
            return 0
    def get_loss_count(self, name):
        if name not in self.df:
            return None
        counts = df[name].value_counts()
        if 'L' in counts:
            return counts['L']
        else:
            return 0
    def get_win_pct(self, name):
        if name not in self.df:
            return None
        wins = self.get_win_count(name)
        losses = self.get_loss_count(name)
        if wins==0:
            return 0.0
        else:
            return wins / (wins+losses)

class ScoringSystem:
    def __init__(self, tourney):
        self.tourney = tourney
    def get_player_scores(self):
        scores = {}
        for name in self.tourney.get_player_names():
            scores[name] = self.get_player_score(name)
        return scores
    def get_player_score(self, name):
        return None

import random

class RandomScorer(ScoringSystem):
    def get_player_score(self, name):
        return random.random()

# http://www.lifewithalacrity.com/2006/01/ranking_systems.html
class ELO(ScoringSystem):
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

def get_scores_per_game(tourney, scoring_system):
    games = tourney.get_games()
    scores = []
    for game_num in range(0, len(games)):
        tourney_so_far = Tourney()
        #print(game_num)
        #print(games[:game_num+1])
        tourney_so_far.set_games(games[0:game_num+1])
        #print(tourney_so_far.get_player_names())
        #new_scores = get_scores(tourney_so_far, scoring_system(tourney_so_far))
        new_scores = scoring_system(tourney_so_far).get_player_scores()
        #print(new_scores)
        scores.append(new_scores)
    return scores

def get_scores_per_game_dataframe(tourney, scoring_system):
    game_scores = get_scores_per_game(tourney, scoring_system)
    scores_df = pandas.DataFrame(game_scores)
    scores_df['Game Summaries'] = tourney.get_game_summaries()
    return scores_df
