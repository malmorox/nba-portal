import customtkinter as ctk
from src.ui.components.team_card import TeamCard
from src.ui.styles.colors import COLORS

class TeamsView(ctk.CTkFrame):
    def __init__(self, parent, data_fetcher, on_team_click=None):
        super().__init__(parent, fg_color=COLORS['bg_dark'])
        
        self.data_fetcher = data_fetcher
        self.on_team_click = on_team_click
        
        self.setup_ui()
        self.load_teams()
    
    def setup_ui(self):
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_dark']
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Grid de 5 columnas
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1, uniform="column")
    
    # Carga y muestra los equipos
    def load_teams(self):
        try:
            teams_df = self.data_fetcher.get_all_teams()
            
            for idx, team in teams_df.iterrows():
                team_data = {
                    'full_name': team['full_name'],
                    'abbreviation': team['abbreviation'],
                    'id': team['id']
                }
                
                row = idx // 5
                col = idx % 5
                
                card = TeamCard(
                    self.scroll_frame,
                    team_data,
                    on_click=self.on_team_click,
                    width=220,
                    height=220
                )
                card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                
        except Exception as e:
            print("Error: ", e)