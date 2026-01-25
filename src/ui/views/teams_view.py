import customtkinter as ctk
from src.ui.components.team_card import TeamCard

class TeamsView(ctk.CTkFrame):
    def __init__(self, parent, data_fetcher, on_team_click=None):
        super().__init__(parent, fg_color="#0d1117")
        
        self.data_fetcher = data_fetcher
        self.on_team_click = on_team_click
        
        self.setup_ui()
        self.load_teams()
    
    def setup_ui(self):
        """Configura la interfaz de la vista"""
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0d1117"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Grid de 5 columnas
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1, uniform="column")
    
    def load_teams(self):
        """Carga y muestra los equipos"""
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
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"❌ Error loading teams: {str(e)}",
                font=ctk.CTkFont(size=16),
                text_color="#f85149"
            )
            error_label.pack(pady=50)