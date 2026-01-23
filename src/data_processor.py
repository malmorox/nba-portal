import pandas as pd

class NBADataProcessor:
    def __init__(self, df):
        self.df = df
    
    def get_basic_info(self):
        info = {
            'Total de registros': len(self.df),
            'Columnas': list(self.df.columns)
        }
        return info
    
    def mostrar_primeros(self, n=10):
        return self.df.head(n)