import customtkinter as ctk
from PIL import Image
from pathlib import Path

class TeamCard(ctk.CTkFrame):
    def __init__(self, parent, team_data, **kwargs):
        super().__init__(parent, corner_radius=15, **kwargs)
        
        self.team_data = team_data
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(fg_color="#21262d")
        
        # Logo del equipo
        self.load_and_display_logo()
        
        # Nombre del equipo
        name_label = ctk.CTkLabel(
            self,
            text=self.team_data['full_name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=180,
            text_color="#c9d1d9"
        )
        name_label.pack(pady=(10, 5))
        
        # Abreviatura
        abbr_label = ctk.CTkLabel(
            self,
            text=self.team_data['abbreviation'],
            font=ctk.CTkFont(size=12),
            text_color="#8b949e"
        )
        abbr_label.pack(pady=(0, 5))
    
    
    # Carga y muestra el logo del equipo
    def load_and_display_logo(self):
        abbr = self.team_data['abbreviation']
        logo_path = Path(f'assets/logos/{abbr}.png')
        
        if logo_path.exists():
            try:
                # Cargar imagen
                pil_image = Image.open(logo_path)
                
                # Redimensionar manteniendo aspecto
                pil_image.thumbnail((100, 100), Image.Resampling.LANCZOS)
                
                # Crear imagen para CustomTkinter
                logo_img = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(100, 100)
                )
                
                logo_label = ctk.CTkLabel(self, image=logo_img, text="")
                logo_label.pack(pady=(20, 5))
                
                # Mantener referencia para evitar garbage collection
                logo_label.image = logo_img
                
            except Exception as e:
                self.show_placeholder(f"Error: {e}")
        else:
            self.show_placeholder("Logo no encontrado")
    
    
    # Muestra un placeholder cuando no hay logo (NO PASA)
    def show_placeholder(self, message=""):
        placeholder = ctk.CTkLabel(
            self,
            text="🏀",
            font=ctk.CTkFont(size=60)
        )
        placeholder.pack(pady=(20, 5))
        
        if message:
            error_label = ctk.CTkLabel(
                self,
                text=message,
                font=ctk.CTkFont(size=9),
                text_color="#6e7681"
            )
            error_label.pack()