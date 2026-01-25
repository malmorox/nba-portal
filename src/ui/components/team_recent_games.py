import customtkinter as ctk

class RecentGamesCard(ctk.CTkFrame):
    
    def __init__(self, parent, games_df, **kwargs):
        super().__init__(parent, fg_color="#161b22", corner_radius=10, **kwargs)
        
        self.games_df = games_df
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="Últimos 10 partidos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        )
        header.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Racha visual
        self.create_streak_visual()
        
        # Separador
        ctk.CTkFrame(self, fg_color="#30363d", height=1)\
            .pack(fill="x", padx=20, pady=10)
        
        # Lista de partidos
        self.create_games_list()
    
    def create_streak_visual(self):
        """Crea visualización de racha (W/L)"""
        streak_frame = ctk.CTkFrame(self, fg_color="transparent")
        streak_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        for idx, row in self.games_df.iterrows():
            is_win = row['IS_WIN']
            
            result_box = ctk.CTkFrame(
                streak_frame,
                fg_color="#238636" if is_win else "#da3633",
                width=35,
                height=35,
                corner_radius=6
            )
            result_box.pack(side="left", padx=2)
            result_box.pack_propagate(False)
            
            ctk.CTkLabel(
                result_box,
                text=row['WL'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white"
            ).pack(expand=True)
    
    def create_games_list(self):
        """Lista detallada de partidos"""
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        for idx, row in self.games_df.iterrows():
            game_item = self.create_game_item(list_frame, row)
            game_item.pack(fill="x", pady=3)
    
    def create_game_item(self, parent, game_data):
        """Crea un item individual de partido"""
        item = ctk.CTkFrame(parent, fg_color="#0d1117", corner_radius=6)
        
        # Contenedor principal
        container = ctk.CTkFrame(item, fg_color="transparent")
        container.pack(fill="x", padx=12, pady=8)
        
        # Fecha (izquierda)
        date_label = ctk.CTkLabel(
            container,
            text=game_data['GAME_DATE'],
            font=ctk.CTkFont(size=12),
            text_color="#8b949e",
            width=80
        )
        date_label.pack(side="left", padx=(0, 15))
        
        # Matchup (centro)
        matchup_label = ctk.CTkLabel(
            container,
            text=game_data['MATCHUP'],
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9",
            anchor="w"
        )
        matchup_label.pack(side="left", fill="x", expand=True)
        
        # Resultado (derecha)
        is_win = game_data['IS_WIN']
        result_color = "#238636" if is_win else "#da3633"
        
        result_label = ctk.CTkLabel(
            container,
            text=f"{game_data['WL']} ({game_data['PTS']})",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=result_color
        )
        result_label.pack(side="right")
        
        return item