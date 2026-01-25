from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats, commonplayerinfo, commonteamroster
import pandas as pd
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parents[2]

class NBADataFetcher:
    def __init__(self, data_dir='data'):
        self.data_dir = BASE_DIR / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_all_teams(self):
        csv_path = self.data_dir / 'nba_teams.csv'
        
        if csv_path.exists():
            return pd.read_csv(csv_path)
        
        # Si no existe, obtenemos de la API (NO PASA)
        teams_data = teams.get_teams()
        df = pd.DataFrame(teams_data)
        df.to_csv(csv_path, index=False)
        return df
    
    
    def get_team_by_id(self, team_id: int) -> dict | None:
        all_teams = self.get_all_teams().to_dict(orient='records')
        for team in all_teams:
            if team['id'] == team_id:
                return team
        return None
    
    def get_team_roster(self, team_id: int, season='2025-26'):
        try:
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=season
            )
            
            df = roster.get_data_frames()[0]
            
            time.sleep(0.6)
            
            return df
            
        except Exception as e:
            print(f"Error obteniendo roster del equipo {team_id}: {e}")
            return pd.DataFrame()