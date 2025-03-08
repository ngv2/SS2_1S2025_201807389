# extract.py
import pandas as pd

def extract():
    # Limpiar pantalla (opcional, por estética)
    print("\033[H\033[J")

    # Pedir la ruta del archivo CSV
    path = input("Ingrese el path del archivo CSV: ")

    try:
        # Leer el CSV con pandas
        df = pd.read_csv(path)
        
        # Mostrar información básica
        print("Número total de registros:", len(df))
        print("\nPrimeras 5 filas:")
        print(df.head())
        input("Presione Enter para continuar...")
        
        print("\nÚltimas 5 filas:")
        print(df.tail())
        input("Presione Enter para continuar...")
        
        # Retornar el DataFrame para que puedas usarlo en la fase de transformación
        return df
    
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        input("Presione Enter para continuar...")
        # Retornar None (o 0) en caso de error, para manejarlo en el main
        return None