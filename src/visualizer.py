import matplotlib.pyplot as plt

class NBAVisualizer:
    def __init__(self, df):
        self.df = df
    
    def mostrar_tabla(self, columnas=None, n=10):
        if columnas:
            df_mostrar = self.df[columnas].head(n)
        else:
            df_mostrar = self.df.head(n)
        
        print(df_mostrar.to_string(index=False))