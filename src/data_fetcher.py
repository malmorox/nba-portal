from nba_api.stats.static import players, teams
import pandas as pd

class NBADataFetcher:
    def __init__(self):
        self.players_data = players.get_players()
        self.teams_data = teams.get_teams()
        self.season = '2025-26'
        
    def get_all_teams(self):
        df = pd.DataFrame(self.teams_data)
        return df
    
    def get_all_players(self):
        df = pd.DataFrame(self.players_data)
        return df