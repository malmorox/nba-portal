from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats, commonplayerinfo, commonteamroster, teamgamelog, boxscoretraditionalv2
import pandas as pd
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parents[2]

class NBADataFetcher:
    def __init__(self, data_dir='data'):
        self.data_dir = BASE_DIR / data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.current_season = '2025-26'
        self._init_config()

    def _init_config(self):
        self.sleep_seconds = 0.6
        self.max_retries = 3
        self.retry_sleep = 1.5

    def _retry_call(self, fn, *args, **kwargs):
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                print(f"[Retry {attempt}/{self.max_retries}] {e}")
                time.sleep(self.retry_sleep)
        raise last_error
    
    def get_all_teams(self):
        csv_path = self.data_dir / 'nba_teams.csv'
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
        else:
            teams_data = teams.get_teams()
            df = pd.DataFrame(teams_data)
            df.to_csv(csv_path, index=False)

        df = df.sort_values(by="full_name").reset_index(drop=True)
        return df
    
    
    def get_team_by_id(self, team_id: int) -> dict | None:
        all_teams = self.get_all_teams().to_dict(orient='records')
        for team in all_teams:
            if team['id'] == team_id:
                return team
        return None
    
    def get_team_roster(self, team_id: int):
        try:
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=self.current_season
            )
            
            df = roster.get_data_frames()[0]
            
            time.sleep(self.sleep_seconds)
            
            return df
            
        except Exception as e:
            print(f"Error obteniendo roster del equipo {team_id}: {e}")
            return pd.DataFrame()
    
    
    def get_team_last_games(self, team_id, last_n=10):
        if last_n <= 0:
            return pd.DataFrame()

        try:
            game_log = self._retry_call(
                teamgamelog.TeamGameLog,
                team_id=team_id,
                season=self.current_season,
                season_type_all_star="Regular Season"
            )

            df = game_log.get_data_frames()[0]
            if df.empty:
                return pd.DataFrame()
            df = df.head(last_n)

            result_df = pd.DataFrame({
                'GAME_DATE': df['GAME_DATE'],
                'MATCHUP': df['MATCHUP'],
                'WL': df['WL'],
                'PTS': df['PTS']
            })
            result_df["IS_WIN"] = result_df["WL"] == "W"

            time.sleep(self.sleep_seconds)
            return result_df

        except Exception as e:
            print(f"Error cargando game log team_id={team_id}: {e}")
            return pd.DataFrame()
    
    def get_top_players_per_game(
        self,
        stat: str = "PTS",
        top_n: int = 5,
        season_type: str = "Regular Season",
        min_gp: int = 5,
    ) -> pd.DataFrame:
        stat = stat.upper().strip()

        try:
            resp = self._retry_call(
                leaguedashplayerstats.LeagueDashPlayerStats,
                season=self.current_season,
                season_type_all_star=season_type,
                per_mode_detailed="PerGame"
            )

            df = resp.get_data_frames()[0]
            if df.empty or stat not in df.columns:
                return pd.DataFrame()

            df = df[df["GP"] >= min_gp]

            result = (
                df.sort_values(by=stat, ascending=False)
                .head(top_n)
                .loc[:, ["PLAYER_NAME", "TEAM_ABBREVIATION", stat]]
                .rename(columns={stat: "VALUE"})
                .reset_index(drop=True)
            )

            return result

        except Exception as e:
            print(f"Error obteniendo TOP {stat}: {e}")
            return pd.DataFrame()