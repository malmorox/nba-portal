import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime

class TeamDetailView(ctk.CTkFrame):
    def __init__(self, parent, team_data, data_fetcher, on_back=None):
        super().__init__(parent, fg_color="#0d1117")
        
        self.team_data = team_data
        self.data_fetcher = data_fetcher
        self.on_back = on_back
        
        self._init_config()
        self.setup_ui()
        self.load_players()
        
    def _init_config(self):
        self.roster_columns = [
            {"weight": 3, "minsize": 250},
            {"weight": 1, "minsize": 100},
            {"weight": 1, "minsize": 130},
            {"weight": 1, "minsize": 80},
        ]
    
    def setup_ui(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#0d1117")
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Botón de volver
        self.create_back_button()
        
        # Sección de información del equipo
        self.create_team_info_section()
        
        # Separador
        self.create_separator()
        
        # Sección de jugadores (header + frame)
        self.create_players_section()
    
    def create_back_button(self):
        back_btn = ctk.CTkButton(
            self.scroll_frame,
            text="← Volver a los equipos",
            command=self.on_back,
            fg_color="#21262d",
            hover_color="#30363d",
            width=150,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        back_btn.pack(anchor="nw", pady=(0, 20))
    
    def create_team_info_section(self):
        team_info_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        team_info_frame.pack(fill="x", pady=(0, 30))
        
        # Container horizontal
        content_container = ctk.CTkFrame(team_info_frame, fg_color="transparent")
        content_container.pack(fill="x", anchor="nw")
        
        # Logo (izquierda)
        self.create_team_logo(content_container)
        
        # Información del equipo (derecha)
        self.create_team_details(content_container)
    
    def create_team_logo(self, parent):
        logo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        logo_frame.pack(side="left", padx=(0, 40), anchor="n")
        
        logo_path = f"assets/logos/{self.team_data['abbreviation']}.png"
        
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_ctk = ctk.CTkImage(
                    light_image=logo_image,
                    dark_image=logo_image,
                    size=(300, 300)
                )
                
                logo_label = ctk.CTkLabel(
                    logo_frame,
                    image=logo_ctk,
                    text=""
                )
                logo_label.pack(padx=20, pady=20)
            except Exception as e:
                self.show_logo_placeholder(logo_frame)
        else:
            self.show_logo_placeholder(logo_frame)
    
    def create_team_details(self, parent):
        info_container = ctk.CTkFrame(parent, fg_color="transparent")
        info_container.pack(side="left", fill="both", expand=True, anchor="n")
        
        # Nombre del equipo
        name_label = ctk.CTkLabel(
            info_container,
            text=self.team_data["full_name"],
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(0, 20))
        
        # Abreviación
        abbr_label = ctk.CTkLabel(
            info_container,
            text=self.team_data['abbreviation'],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#8b949e",
            anchor="w"
        )
        abbr_label.pack(anchor="w", pady=(0, 15))
        
        # Ciudad y Estado
        city_state = f"{self.team_data['city']}, {self.team_data.get('state', 'N/A')}"
        location_label = ctk.CTkLabel(
            info_container,
            text=city_state,
            font=ctk.CTkFont(size=18),
            text_color="#c9d1d9",
            anchor="w"
        )
        location_label.pack(anchor="w", pady=(0, 15))
        
        # Fundado
        founded_label = ctk.CTkLabel(
            info_container,
            text=f"Fundado en {self.team_data['year_founded']}",
            font=ctk.CTkFont(size=16),
            text_color="#8b949e",
            anchor="w"
        )
        founded_label.pack(anchor="w", pady=(0, 20))
    
    def create_separator(self):
        separator = ctk.CTkFrame(self.scroll_frame, fg_color="#30363d", height=2)
        separator.pack(fill="x", pady=30)
    
    def create_players_section(self):
        # Header
        players_header = ctk.CTkLabel(
            self.scroll_frame,
            text="Plantilla",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        )
        players_header.pack(anchor="w", pady=(0, 20))
        
        # Frame para jugadores
        self.players_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.players_frame.pack(fill="both", expand=True)
    
    def load_players(self):
        """Carga los jugadores usando pandas"""
        try:
            # Obtener roster como DataFrame
            roster_df = self.data_fetcher.get_team_roster(self.team_data['id'])
            
            if not roster_df.empty:
                self.display_players(roster_df)
            else:
                self.show_no_players_message()
                
        except Exception as e:
            print(f"Error loading players: {e}")
            self.show_error_message(str(e))
    
    def display_players(self, roster_df):
        # Limpiar frame
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        
        self.create_players_header()

        for idx, row in roster_df.iterrows():
            player_row = self.create_player_row(
                self.players_frame,
                player_data = {
                    'name': row['PLAYER'],
                    'number': row['NUM'],
                    'position': row['POSITION'],
                    'height': row['HEIGHT'],
                    'weight': row['WEIGHT'],
                    'birth_date': row['BIRTH_DATE'],
                    'age': row['AGE']
                }
            )
            player_row.pack(fill="x", pady=4)
    
    
    def create_players_header(self):
        header = ctk.CTkFrame(self.players_frame, fg_color="#161b22", height=40)
        header.pack(fill="x", pady=(0, 0))
        header.pack_propagate(False)

        grid_container = ctk.CTkFrame(header, fg_color="transparent")
        grid_container.pack(fill="both", expand=True)
        
        grid_container.grid_columnconfigure(0, weight=3, minsize=250)
        grid_container.grid_columnconfigure(1, weight=1, minsize=100)
        grid_container.grid_columnconfigure(2, weight=1, minsize=130)
        grid_container.grid_columnconfigure(3, weight=1, minsize=80)

        columns = ["Jugador", "Altura", "Fecha de nacimiento", "Edad"]

        for col, text in enumerate(columns):
            lbl = ctk.CTkLabel(
                grid_container,
                text=text,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#8b949e",
                anchor="w"
            )
            lbl.grid(row=0, column=col, sticky="w", padx=15, pady=8)
    
    def create_player_row(self, parent, player_data):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x")

        row = ctk.CTkFrame(container, fg_color="#0d1117", height=48)
        row.pack(fill="x")
        row.pack_propagate(False)

        for i, col in enumerate(self.roster_columns):
            row.grid_columnconfigure(
                i, weight=col["weight"], minsize=col["minsize"]
            )

        ctk.CTkLabel(
            row,
            text=f"#{player_data['number']}  {player_data['name']} ({player_data['position']})",
            font=ctk.CTkFont(size=14),
            text_color="#c9d1d9",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=15)

        ctk.CTkLabel(
            row,
            text=player_data['height'],
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        ).grid(row=0, column=1, sticky="w", padx=15)

        ctk.CTkLabel(
            row,
            text=format_birth_date(player_data['birth_date']),
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        ).grid(row=0, column=2, sticky="w", padx=15)

        ctk.CTkLabel(
            row,
            text=f"{int(player_data['age'])} años",
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        ).grid(row=0, column=3, sticky="w", padx=15)

        # Línea separadora
        ctk.CTkFrame(container, fg_color="#30363d", height=1)\
            .pack(fill="x", padx=10, pady=(0, 4))

        return container
    
    def show_no_players_message(self):
        message = ctk.CTkLabel(
            self.players_frame,
            text="No roster data available for this season",
            font=ctk.CTkFont(size=14),
            text_color="#6e7681"
        )
        message.pack(pady=50)
    
    def show_error_message(self, error):
        """Muestra mensaje de error"""
        message = ctk.CTkLabel(
            self.players_frame,
            text=f"❌ Error loading roster: {error}",
            font=ctk.CTkFont(size=14),
            text_color="#f85149"
        )
        message.pack(pady=50)
    
    def show_logo_placeholder(self, parent):
        """Muestra placeholder cuando no hay logo"""
        placeholder = ctk.CTkLabel(
            parent,
            text="🏀",
            font=ctk.CTkFont(size=120),
            text_color="#8b949e",
            width=300,
            height=300
        )
        placeholder.pack(padx=20, pady=20)
        

def format_birth_date(raw_date):
    try:
        dt = datetime.strptime(raw_date, "%b %d, %Y")
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return raw_date