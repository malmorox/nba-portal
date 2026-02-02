import customtkinter as ctk
from PIL import Image
from pathlib import Path
from src.ui.styles.colors import COLORS

class TeamCard(ctk.CTkFrame):
    def __init__(self, parent, team_data, on_click=None, width=220, height=220):
        super().__init__(
            parent, 
            corner_radius=15, 
            width=width,
            height=height,
            cursor="hand2")
        
        self.team_data = team_data
        self.on_click = on_click
        
        self.setup_ui()
        
        self.bind("<Button-1>", self.handle_click)
        for child in self.winfo_children():
            child.bind("<Button-1>", self.handle_click)
    
    def setup_ui(self):
        self.configure(fg_color=COLORS['cards_or_buttons_primary'])
        
        # Logo del equipo
        self.load_and_display_logo()
        
        # Nombre del equipo
        name_label = ctk.CTkLabel(
            self,
            text=self.team_data['full_name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=180,
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(10, 5))
        
        # Abreviatura
        abbr_label = ctk.CTkLabel(
            self,
            text=self.team_data['abbreviation'],
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        abbr_label.pack(pady=(0, 5))
    
    
    # Carga y muestra el logo del equipo a partir de la abreviación
    def load_and_display_logo(self):
        abbr = self.team_data['abbreviation']
        logo_path = Path(f'assets/logos/{abbr}.png')
        
        if logo_path.exists():
            try:
                # Cargar imagen con PIL
                pil_image = Image.open(logo_path)
                
                # Redimensionando manteniendo aspecto
                pil_image.thumbnail((100, 100), Image.Resampling.LANCZOS)
                
                logo_img = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(100, 100)
                )
                
                logo_label = ctk.CTkLabel(self, image=logo_img, text="")
                logo_label.pack(pady=(20, 5))
                
                logo_label.image = logo_img
                
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Logo no encontrado")
    
    def handle_click(self, event):
        if self.on_click:
            self.on_click(self.team_data["id"])