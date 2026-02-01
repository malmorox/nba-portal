import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, stat, data_fetcher):
        super().__init__(
            parent,
            fg_color="#161b22",
            corner_radius=14
        )

        self.stat = stat
        self.data_fetcher = data_fetcher

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w")

        self.draw_chart()

    def draw_chart(self):
        df = self.data_fetcher.get_top_players_per_game(
            stat=self.stat,
            top_n=5
        )

        if df.empty:
            ctk.CTkLabel(
                self,
                text="No hay datos disponibles",
                text_color="gray"
            ).pack(pady=20)
            return

        players = df["PLAYER_NAME"][::-1]
        values = df["VALUE"][::-1]

        fig = Figure(figsize=(10, 3), dpi=100)
        ax = fig.add_subplot(111)

        # Horizontal bar chart (ranking)
        ax.barh(players, values)

        ax.set_xlabel(f"{self.stat} por partido")
        ax.set_ylabel("")
        ax.grid(axis="x", linestyle="--", alpha=0.3)

        # Limpieza visual
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=20, pady=(5, 20))