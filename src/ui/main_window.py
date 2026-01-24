import customtkinter as ctk
from src.core.data_fetcher import NBADataFetcher
from src.ui.components.team_card import TeamCard

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("NBA Teams")
        self.geometry("1400x900")
        
        # Tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Color de fondo
        self.configure(fg_color="#0d1117")
        
        # Inicializar data fetcher
        self.data_fetcher = NBADataFetcher()
        
        # Configurar UI
        self.setup_ui()
        
        # Cargar equipos
        self.load_teams()
    
    def setup_ui(self):
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0d1117"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Grid de 5 columnas
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1, uniform="column")
    
    def load_teams(self):
        try:
            teams_df = self.data_fetcher.get_all_teams()
            
            # Crear tarjetas
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
                    width=220,
                    height=220
                )
                card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"❌ Error: {str(e)}",
                font=ctk.CTkFont(size=16),
                text_color="#f85149"
            )
            error_label.pack(pady=50)