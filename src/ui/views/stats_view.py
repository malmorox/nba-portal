import customtkinter as ctk
from src.ui.components.stat_card import StatCard
from src.ui.components.chart_types import ChartType
from src.ui.styles.colors import COLORS

class StatsView(ctk.CTkFrame):
    def __init__(self, parent, data_fetcher):
        super().__init__(parent, fg_color=COLORS['bg_dark'])

        self.data_fetcher = data_fetcher

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.build_stats()

    def build_stats(self):
        stats = [
            ("5 máximos anotadores", "PTS", ChartType.BARH),
            ("5 máximos reboteadores", "REB", ChartType.LINE),
            ("5 máximos asistentes", "AST", ChartType.DONUT),
            ("5 máximos tapones", "BLK", ChartType.BARH),
            ("5 máximos robos", "STL", ChartType.LINE),
        ]

        for title, stat, chart_type in stats:
            card = StatCard(
                self.scroll,
                title=title,
                stat=stat,
                chart_type=chart_type,
                data_fetcher=self.data_fetcher
            )
            card.pack(fill="x", pady=20)