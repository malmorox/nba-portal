from src.data_fetcher import NBADataFetcher
from src.data_processor import NBADataProcessor
from src.visualizer import NBAVisualizer

def main():
    print("--ESTADÍSTICAS NBA--\n")
    
    fetcher = NBADataFetcher()
    df_teams = fetcher.get_all_teams()
    
    print(f"Equipos obtenidos: {len(df_teams)}\n")
    
    processor = NBADataProcessor(df_teams)
    info = processor.get_basic_info()
    print(f"Total: {info['Total de registros']}")
    print(f"Columnas: {info['Columnas']}\n")
    
    print("EQUIPOS NBA:\n")
    visualizer = NBAVisualizer(df_teams)
    visualizer.mostrar_tabla(columnas=['full_name', 'abbreviation', 'city'], n=30)

if __name__ == "__main__":
    main()