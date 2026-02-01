import customtkinter as ctk
from src.ui.components.stat_card import StatCard

class StatsView(ctk.CTkFrame):
    def __init__(self, parent, data_fetcher):
        super().__init__(parent, fg_color="#0d1117")

        self.data_fetcher = data_fetcher

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.build_stats()

    def build_stats(self):
        stats = [
            ("5 máximos anotadores", "PTS"),
            ("5 máximos reboteadores", "REB"),
            ("5 máximos asistentes", "AST"),
            ("5 máximos tapones", "BLK"),
            ("5 máximos robos", "STL"),
        ]

        for title, stat in stats:
            chart = StatCard(
                self.scroll,
                title=title,
                stat=stat,
                data_fetcher=self.data_fetcher
            )
            chart.pack(fill="x", pady=20)