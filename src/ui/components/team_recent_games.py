from src.core.data_processor import NBADataProcessor
import customtkinter as ctk
from PIL import Image
import os

class RecentGamesCard(ctk.CTkFrame):

    def __init__(self, parent, games_df, title="Últimos 10 partidos", **kwargs):
        super().__init__(parent, fg_color="#161b22", corner_radius=10, **kwargs)
        self.games_df = games_df
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text=self.title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        )
        header.pack(anchor="w", padx=20, pady=(15, 10))

        # Lista de partidos
        self.create_last_games_list()

    def create_last_games_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        for _, row in self.games_df.iterrows():
            self.create_game_item(list_frame, row).pack(fill="x", pady=6)

    def _get_opponent_abbr(self, matchup: str) -> str:
        if not matchup:
            return "UNK"
        parts = matchup.replace("vs.", "vs").split()
        return parts[-1].strip()
    
    def _get_team_logo(self, abbr: str, size=(20, 20)):
        if not abbr:
            return None

        logo_path = f"assets/logos/{abbr}.png"
        if not os.path.exists(logo_path):
            return None

        try:
            img = Image.open(logo_path)
            return ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=size
            )
        except Exception:
            return None


    def create_game_item(self, parent, game_data):
        is_win = bool(game_data.get("IS_WIN", False))
        wl = str(game_data.get("WL", ""))
        date_text = str(game_data.get("GAME_DATE", ""))

        opponent = self._get_opponent_abbr(str(game_data.get("MATCHUP", "")))

        # Colores
        row_bg = "#0d1117"
        primary = "#ffffff" if is_win else "#c9d1d9"
        muted = "#6e7681"
        badge_bg = "#238636" if is_win else "#da3633"

        item = ctk.CTkFrame(parent, fg_color=row_bg, corner_radius=8)

        container = ctk.CTkFrame(item, fg_color="transparent")
        container.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(
            container,
            text=NBADataProcessor.format_birth_date(date_text),
            font=ctk.CTkFont(size=12),
            text_color=muted,
            width=95,
            anchor="w"
        ).pack(side="left", padx=(0, 14))

        matchup_container = ctk.CTkFrame(container, fg_color="transparent")
        matchup_container.pack(side="left", fill="x", expand=True)
        # logo rival
        logo_img = self._get_team_logo(opponent)
        
        ctk.CTkLabel(
            matchup_container,
            text="vs",
            font=ctk.CTkFont(size=13),
            text_color=muted,
            anchor="w"
        ).pack(side="left", padx=(0, 6))

        if logo_img:
            ctk.CTkLabel(
                matchup_container,
                image=logo_img,
                text=""
            ).pack(side="left")

        ctk.CTkLabel(
            matchup_container,
            text=opponent,
            font=ctk.CTkFont(size=15),
            text_color=primary,
            anchor="w"
        ).pack(side="left", padx=(2, 0))

        badge = ctk.CTkFrame(
            container,
            fg_color=badge_bg,
            corner_radius=8,
            width=34,
            height=26
        )
        badge.pack(side="right")
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text=wl,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        ).pack(expand=True)

        return item