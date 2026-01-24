from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats, commonplayerinfo
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
    
    
    # Información detallada de un jugador
    def get_player_info(self, player_id):
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            df = info.get_data_frames()[0]
            time.sleep(0.6)
            return df
        except Exception as e:
            print(f"Error obteniendo info del jugador {player_id}: {e}")
            return None
    
    # Obtiene estadísticas de toda la carrera de un jugador
    def get_player_career_stats(self, player_id):
        try:
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            df = career.get_data_frames()[0]  # [0] = regular season, [1] = playoffs
            time.sleep(0.6)
            return df
        except Exception as e:
            print(f"Error obteniendo stats del jugador {player_id}: {e}")
            return None