import customtkinter as ctk
from src.core.data_fetcher import NBADataFetcher
from src.core.data_processor import NBADataProcessor
from src.ui.views.stats_view import StatsView
from src.ui.views.teams_view import TeamsView
from src.ui.views.team_detail_view import TeamDetailView
from src.ui.styles.colors import COLORS

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Portal NBA")
        self.geometry("1400x900")
        
        # Tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Color de fondo
        self.configure(fg_color=COLORS['bg_dark'])
        
        self.data_fetcher = NBADataFetcher()

        self.data_processor = NBADataProcessor()
        
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        self.main_container.pack(fill="both", expand=True)
        
        self.setup_ui()
        
        # Mostrar vista inicial
        self.show_view('teams')
    
    def setup_ui(self):
        # Header con navegación
        self.header = ctk.CTkFrame(self.main_container, fg_color=COLORS['bg_medium'], height=60)
        self.header.pack(fill="x", padx=0, pady=0)
        self.header.pack_propagate(False)
        
        # Botones de navegación
        nav_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        nav_frame.pack(side="left", padx=20, pady=10)
        
        self.nav_buttons = {
            'stats': ctk.CTkButton(
                nav_frame,
                text="Estadísticas",
                command=lambda: self.show_view('stats'),
                width=120,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            ),
            'teams': ctk.CTkButton(
                nav_frame,
                text="Equipos",
                command=lambda: self.show_view('teams'),
                width=120,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            )
        }
        
        for btn in self.nav_buttons.values():
            btn.pack(side="left", padx=5)
        
        # Content container
        self.content_container = ctk.CTkFrame(self.main_container, fg_color=COLORS['bg_dark'])
        self.content_container.pack(fill="both", expand=True)
        
        # Vista actual
        self.current_view = None
    
    def update_nav_buttons(self, active_view):
        for key, btn in self.nav_buttons.items():
            if key == active_view:
                btn.configure(fg_color=COLORS['primary'], hover_color=COLORS['secondary'])
            else:
                btn.configure(fg_color=COLORS['cards_or_buttons_primary'], hover_color=COLORS['cards_or_buttons_secondary'])
    
    
    def clear_content(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    
    # Muestra la vista que se pasa por parametro
    def show_view(self, view_name):
        self.clear_content()
        self.update_nav_buttons(view_name)
        
        if view_name == 'stats':
            self.current_view = StatsView(
                self.content_container,
                self.data_fetcher
            )
        
        elif view_name == 'teams':
            self.current_view = TeamsView(
                self.content_container, 
                self.data_fetcher,
                on_team_click=self.show_team_detail
            )
        
        if self.current_view:
            self.current_view.pack(fill="both", expand=True)
    
    # Muestra los detalles de un equipo
    def show_team_detail(self, team_id: int):
        self.clear_content()
        
        team = self.data_fetcher.get_team_by_id(team_id)
        
        if team:
            self.current_view = TeamDetailView(
                self.content_container,
                team,
                self.data_fetcher,
                self.data_processor,
                on_back=lambda: self.show_view('teams')
            )
            self.current_view.pack(fill="both", expand=True)