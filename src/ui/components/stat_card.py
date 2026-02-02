import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
from src.ui.components.chart_types import ChartType
from src.ui.styles.colors import COLORS

class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, stat, chart_type: ChartType, data_fetcher):
        super().__init__(parent, fg_color=COLORS['bg_medium'], corner_radius=14)

        self.stat = stat
        self.chart_type = chart_type
        self.data_fetcher = data_fetcher

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w")

        self.build_chart()

    def build_chart(self):
        df = self.data_fetcher.get_top_players_per_game(stat=self.stat, top_n=5)

        if df.empty:
            self.empty()
            return

        fig = Figure(figsize=(10, 3), dpi=100)
        ax = fig.add_subplot(111)
        # Depende del tipo de grafico dibuja uno u otro
        if self.chart_type == ChartType.BARH:
            self.draw_barh(ax, df)
        elif self.chart_type == ChartType.LINE:
            self.draw_line(ax, df)
        elif self.chart_type == ChartType.DONUT:
            self.draw_donut(ax, df)
        else:
            self.empty()
            return

        fig.tight_layout()
        FigureCanvasTkAgg(fig, self).get_tk_widget().pack(fill="x", padx=20, pady=(5, 20))

    def empty(self):
        ctk.CTkLabel(
            self,
            text="No hay datos disponibles",
            text_color=COLORS['text_secondary']
        ).pack(pady=20)

    def draw_barh(self, ax, df):
        players = df["PLAYER_NAME"][::-1]
        values = df["VALUE"][::-1]

        ax.barh(players, values)
        ax.set_xlabel(f"{self.stat} por partido")
        ax.grid(axis="x", linestyle="--", alpha=0.3)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    def draw_line(self, ax, df):
        players = df["PLAYER_NAME"]
        values = df["VALUE"]

        ax.plot(players, values, marker="o", linewidth=2)
        ax.set_ylabel(f"{self.stat} por partido")
        ax.grid(True, linestyle="--", alpha=0.3)

        ax.tick_params(axis="x", labelrotation=25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    def draw_donut(self, ax, df):
        wedges, _ = ax.pie(df["VALUE"], startangle=90)
        ax.add_artist(Circle((0, 0), 0.6))
        ax.set_aspect("equal")
        ax.legend(
            wedges,
            df["PLAYER_NAME"],
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=False
        )