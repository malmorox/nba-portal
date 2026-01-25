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
    
    
    def get_team_last_games(self, team_id, last_n=10):
        cache_key = f"last_games_{team_id}_{last_n}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            from nba_api.stats.endpoints import teamgamelog
            
            game_log = teamgamelog.TeamGameLog(
                team_id=team_id,
                season=self.current_season,
                season_type_all_star='Regular Season'
            )
            
            df = game_log.get_data_frames()[0]
            df = df.head(last_n)
            
            # Limpiar y formatear datos
            result_df = pd.DataFrame({
                'GAME_DATE': pd.to_datetime(df['GAME_DATE']).dt.strftime('%d/%m/%Y'),
                'MATCHUP': df['MATCHUP'],
                'WL': df['WL'],
                'PTS': df['PTS'],
                'IS_WIN': df['WL'] == 'W'
            })
            
            self.cache[cache_key] = result_df
            return result_df
            
        except Exception as e:
            print(f"Error loading game log: {e}")
            return pd.DataFrame()