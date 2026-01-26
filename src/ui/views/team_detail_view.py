from src.ui.components.team_recent_games import RecentGamesCard
import customtkinter as ctk
from PIL import Image
import os

class TeamDetailView(ctk.CTkFrame):
    def __init__(self, parent, team_data, data_fetcher, data_processor, on_back=None):
        super().__init__(parent, fg_color="#0d1117")
        
        self.team_data = team_data
        self.data_fetcher = data_fetcher
        self.data_processor = data_processor
        self.on_back = on_back
        
        self._init_config()
        self.setup_ui()
        self.load_recent_games()
        self.load_players()
        
    def _init_config(self):
        self.roster_columns = [
            {"weight": 3, "minsize": 250},
            {"weight": 1, "minsize": 100},
            {"weight": 1, "minsize": 130},
            {"weight": 1, "minsize": 80},
        ]
        self.recent_games_column_width = 360
    
    def setup_ui(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#0d1117")
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Botón de volver
        self.create_back_button()
        
        # Sección de información del equipo
        self.create_team_info_section()
        
        # Separador
        self.create_separator()

        self.create_bottom_layout()
    
    # BOTON DE VOLVER A LA PESATÑA DE EQUIPOS
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
    
    # SECCION SUPERIOR CON LA INFORMACIÓN DE CADA EQUIPO
    def create_team_info_section(self):
        team_info_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        team_info_frame.pack(fill="x")
        
        # Container horizontal
        content_container = ctk.CTkFrame(team_info_frame, fg_color="transparent")
        content_container.pack(fill="x", anchor="nw")
        
        # Logo (izquierda)
        self.display_team_logo(content_container)
        
        # Información del equipo (derecha)
        self.display_team_details(content_container)
    
    # FUNCION PARA CARGAR EL LOGO DEL EQUIPO A PARTIR DE LA ABREVIACIÓN DEL EQUIPO
    def display_team_logo(self, parent):
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
    
    # FUNCION PARA CARGAR LOS DETALLES DEL EQUIPO (NOMBRE, ABREVIACIÓN CIUDAD, ESTADO, AÑO DE FUNDACIÓN Y ESTADIO)
    def display_team_details(self, parent):
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
    
    # SEPARADOR QUE DIVIDE LA INFORMACIÓN DEL EQUIPO DE LA PLATILLA Y ULTIMOS PARTIDOS JUGADOS 
    def create_separator(self):
        separator = ctk.CTkFrame(self.scroll_frame, fg_color="#30363d", height=2)
        separator.pack(fill="x", pady=30)
    

    def create_bottom_layout(self):
        bottom_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        bottom_container.pack(fill="both", expand=True)

        # Columna izquierda - Partidos recientes
        self.recent_col = ctk.CTkFrame(
            bottom_container,
            fg_color="transparent",
            width=self.recent_games_column_width
        )
        self.recent_col.pack(side="left", fill="y", padx=(0, 20), anchor="n")
        self.recent_col.pack_propagate(False)

        # Frame de partidos recientes que se ajusta al contenido
        self.recent_games_frame = ctk.CTkFrame(
            self.recent_col,
            fg_color="#161b22",
            corner_radius=10
        )
        self.recent_games_frame.pack(fill="x", expand=False)

        self.recent_placeholder = ctk.CTkLabel(
            self.recent_games_frame,
            text="(Aquí irán los últimos 10 partidos)",
            font=ctk.CTkFont(size=13),
            text_color="#6e7681"
        )
        self.recent_placeholder.pack(expand=True, pady=20)  # Añadido pady para dar espacio

        # Columna derecha - Jugadores
        self.players_col = ctk.CTkFrame(bottom_container, fg_color="transparent")
        self.players_col.pack(side="left", fill="both", expand=True, anchor="n")

        self.create_players_section()
    
    def load_recent_games(self):
        try:
            games_df = self.data_fetcher.get_team_last_games(
                team_id=self.team_data["id"],
                last_n=10
            )

            if games_df is None or games_df.empty:
                self.show_recent_games_empty()
                return

            self.display_recent_games(games_df)

        except Exception as e:
            print(f"Error loading recent games: {e}")
            self.show_recent_games_error(str(e))


    def display_recent_games(self, games_df):
    # limpiar placeholder / widgets anteriores
        for w in self.recent_games_frame.winfo_children():
            w.destroy()

        # UNA sola card que ya contiene header + racha + lista
        card = RecentGamesCard(
            self.recent_games_frame,
            games_df=games_df,
            width=self.recent_games_column_width
        )
        card.pack(fill="both", expand=True)


    def show_recent_games_empty(self):
        for w in self.recent_games_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.recent_games_frame,
            text="No hay partidos recientes disponibles.",
            font=ctk.CTkFont(size=13),
            text_color="#6e7681",
            justify="left"
        ).pack(padx=15, pady=15, anchor="w")

    def show_recent_games_error(self, error):
        for w in self.recent_games_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.recent_games_frame,
            text=f"❌ Error cargando partidos:\n{error}",
            font=ctk.CTkFont(size=13),
            text_color="#f85149",
            justify="left"
        ).pack(padx=15, pady=15, anchor="w")

    # SECCIÓN PARA CARGAR LOS JUGADORES DEL EQUIPO SELECCIONADO
    def create_players_section(self):
        # Header
        players_header = ctk.CTkLabel(
            self.players_col,
            text="Plantilla",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        )
        players_header.pack(anchor="w", pady=(0, 20))
        
        # Frame para jugadores
        self.players_frame = ctk.CTkFrame(self.players_col, fg_color="transparent")
        self.players_frame.pack(fill="both", expand=True)
    
    def load_players(self):
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

        player_info_frame = ctk.CTkFrame(row, fg_color="transparent")
        player_info_frame.grid(row=0, column=0, sticky="w", padx=15, pady=10)

        # Número en círculo
        number_circle = ctk.CTkFrame(
            player_info_frame,
            fg_color="#30363d",
            width=40,
            height=40,
            corner_radius=20
        )
        number_circle.pack(side="left", padx=(0, 12))
        number_circle.pack_propagate(False)

        ctk.CTkLabel(
            number_circle,
            text=f"{player_data['number']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#c9d1d9"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Nombre y posición (vertical)
        name_container = ctk.CTkFrame(player_info_frame, fg_color="transparent")
        name_container.pack(side="left")

        ctk.CTkLabel(
            name_container,
            text=player_data['name'],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#c9d1d9",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            name_container,
            text=player_data['position'],
            font=ctk.CTkFont(size=12),
            text_color="#8b949e",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            row,
            text=player_data['height'],
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        ).grid(row=0, column=1, sticky="w", padx=15)

        ctk.CTkLabel(
            row,
            text=self.data_processor.format_birth_date(player_data['birth_date']),
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
        message = ctk.CTkLabel(
            self.players_frame,
            text=f"❌ Error loading roster: {error}",
            font=ctk.CTkFont(size=14),
            text_color="#f85149"
        )
        message.pack(pady=50)
    
    def show_logo_placeholder(self, parent):
        placeholder = ctk.CTkLabel(
            parent,
            text="🏀",
            font=ctk.CTkFont(size=120),
            text_color="#8b949e",
            width=300,
            height=300
        )
        placeholder.pack(padx=20, pady=20)