import re
import json
import pandas
import statistics
import itertools
import math

def parse_games(string):
    games = []
    lines = string.split("\n")
    #print(lines)
    pattern = re.compile(r"^([\s]*(?P<winner>[\w]+)[\s]*,?)+ (over|beat) ([\s]*(?P<loser>[\w]+)[\s]*,?)+( on (?P<time>.*))?$", re.IGNORECASE)
    for line in lines:
        if line.strip()=='':
            pass
        else:
            #matches = re.match(r"(?P<winners>.*) over (?P<losers>.*)( on (?P<time>.*))?",line)
            matches = re.match(r"(?P<winners>.*) over (?P<losers>.*)", line, re.IGNORECASE)
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
        return self.df.copy()
    def get_player_names(self):
        return list(self.df)
    def get_win_count(self, name):
        if name not in list(self.df):
            return 0
        counts = self.df[name].value_counts()
        if 'W' in counts:
            return counts['W']
        else:
            return 0
    def get_loss_count(self, name):
        if name not in self.df:
            return 0
        counts = self.df[name].value_counts()
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

    def get_all_possible_games(self, players=None):
        games = []
        teams_seen = []
        if not players:
            players = self.get_player_names()
        team_as = itertools.combinations(players, math.ceil(len(players)/2))
        for team_a in team_as:
            if set(team_a) not in teams_seen:
                teams_seen.append(set(team_a))
                team_b = tuple(set(players) - set(team_a))
                teams_seen.append(set(team_b))
                games.append((team_a, team_b))
        return games

    def get_possible_games(self, players_per_team, players=None):
        games = []
        if not players:
            players = self.get_player_names()
        games_players = itertools.combinations(players, players_per_team * 2)
        for players in games_players:
            team_combos = itertools.combinations(players,players_per_team)
            teams_seen = []
            for team_a in team_combos:
                if set(team_a) not in teams_seen:
                    teams_seen.append(set(team_a))
                    team_b = tuple(set(players) - set(team_a))
                    teams_seen.append(set(team_b))
                    games.append((team_a, team_b))
        return games
    def get_possible_teams(self, players_per_team, players=None):
        if not players:
            players = self.get_player_names()
        return list(itertools.combinations(players, players_per_team))

    def get_unplayed_teams(self, players_per_team, players=None):
        """Teams that have not yet played"""
        if not players:
            players = self.get_player_names()
        combos = self.get_possible_teams(players_per_team, players=players)
        teams = itertools.filterfalse(self.has_team_played, combos)
        return list(teams)

    def has_team_played(self, team):
        for game in self.games:
            if set(team) == set(game['winners']) or set(team) == set(game['losers']):
                return True
        return False

    def has_combo_played(self, combo):
        for game in self.games:
            if set(combo[0]) == set(game['winners']) and set(combo[1]) == set(game['losers']):
                return True
            if set(combo[1]) == set(game['winners']) and set(combo[0]) == set(game['losers']):
                return True
        return False
    #def get_possible_unplayed_games(self, players_per_team, players=None):
    #    combos = self.get_possible_games(players_per_team, players=players)
    #    combos[:] = itertools.filterfalse(self.has_combo_played, combos)
        




    def get_pvp_win_df(self):
        """Get DataFrame as grid showing how many times player won against another
        
        Build DataFrame such as:
                        Subject   Bob  Maea  Dean  Sean
        Other Relationship Type    
        Bob   Together     Won      9     3     2     2
                           Lost     4     1     0     3
              Against      Won      0     2     6     2
                           Lost     0     1     9     3
        ...
        Won/Lost is from the perspective of the column
        """
        players = self.get_player_names()
        indexes = pandas.MultiIndex.from_product( \
            [players,("Together","Against"),("Played","Won","Lost")], \
            names=("Other","Relationship","Type"))
        df = pandas.DataFrame(columns=players, index=indexes)
        for col in df.columns:
            df[col].values[:] = 0
        #print(df)
        for game in self.games:
            for combo in list(itertools.combinations_with_replacement(game['winners'],2)):
                df[combo[0]][(combo[1],"Together","Played")] += 1
                df[combo[0]][(combo[1],"Together","Won")] += 1
                if combo[0] != combo[1]:
                    df[combo[1]][(combo[0],"Together","Played")] += 1
                    df[combo[1]][(combo[0],"Together","Won")] += 1
            for combo in list(itertools.combinations_with_replacement(game['losers'],2)):
                df[combo[0]][(combo[1],"Together","Played")] += 1
                df[combo[0]][(combo[1],"Together","Lost")] += 1
                if combo[0] != combo[1]:
                    df[combo[1]][(combo[0],"Together","Played")] += 1
                    df[combo[1]][(combo[0],"Together","Lost")] += 1
            for winner in game['winners']:
                for loser in game['losers']:
                    df[winner][(loser,"Against","Played")] += 1
                    df[winner][(loser,"Against","Won")] += 1
                    df[loser][(winner,"Against","Played")] += 1
                    df[loser][(winner,"Against","Lost")] += 1
        return df

    def get_player_stats(self, name, scoring_system=None):
        stats = {}
        stats['name'] = name
        wins = self.get_win_count(name)
        losses = self.get_loss_count(name)
        stats['games'] = wins + losses
        stats['wins'] = wins
        stats['losses'] = losses
        if wins == 0: stats['win pct'] = 0.0
        else: stats['win pct'] = wins / (wins + losses)
        if scoring_system:
            stats['score'] = scoring_system(self).get_player_score(name)
        return stats

    def get_all_player_stats(self, scoring_system=None):
        stats = []
        for player in self.get_player_names():
            stats.append(self.get_player_stats(player, scoring_system))
        return stats
    
    def get_all_player_stats_dataframe(self, scoring_system=None):
        return pandas.DataFrame(self.get_all_player_stats(scoring_system)).set_index('name')





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
