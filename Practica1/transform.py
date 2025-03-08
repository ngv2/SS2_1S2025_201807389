import pandas as pd

def transform(df):
    # Limpiar pantalla
    print("\033[H\033[J")

    # --- Limpieza de datos ---
    # Reemplazar valores "0" o "-" en 'Arrival Airport' por un valor por defecto
    df['Arrival Airport'] = df['Arrival Airport'].replace(["0", "-"], "No especificado")

    # --- Normalización de Fechas ---
    def parse_dates(date_str):
        for fmt in ('%m/%d/%Y', '%m-%d-%Y'):
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    # Convertir 'Departure Date' a formato datetime
    df['Departure Date'] = df['Departure Date'].apply(parse_dates)

    # --- Creación de Dimensiones ---

    # Dimensión de Fecha de Salida
    dim_departure_date = df[['Departure Date']].drop_duplicates().copy()
    dim_departure_date['DepartureDateID'] = range(1, len(dim_departure_date) + 1)
    dim_departure_date['Year']  = dim_departure_date['Departure Date'].dt.year
    dim_departure_date['Month'] = dim_departure_date['Departure Date'].dt.month
    dim_departure_date['Day']   = dim_departure_date['Departure Date'].dt.day
    print("DimDepartureDate:")
    print(dim_departure_date.head())
    input("Presione Enter para continuar...")

    # Dimensión de Aeropuerto de Llegada
    dim_arrival_airport = df[['Arrival Airport']].drop_duplicates().copy()
    dim_arrival_airport['ArrivalAirportID'] = range(1, len(dim_arrival_airport) + 1)
    
    # Dimensión de Pilotos
    dim_pilot = df[['Pilot Name']].drop_duplicates().copy()
    dim_pilot['PilotID'] = range(1, len(dim_pilot) + 1)
    
    # Dimensión de Estado del Vuelo
    dim_flight_status = df[['Flight Status']].drop_duplicates().copy()
    dim_flight_status['FlightStatusID'] = range(1, len(dim_flight_status) + 1)
    print("DimFlightStatus:")
    print(dim_flight_status.head())
    input("Presione Enter para continuar...")

    # Dimensión de Aeropuerto de Salida
    dim_departure_airport = df[['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent', 'Continents']].drop_duplicates().copy()
    dim_departure_airport['DepartureAirportID'] = range(1, len(dim_departure_airport) + 1)
    # En caso de que existan registros duplicados considerando solo 'Airport Name'
    dim_departure_airport = dim_departure_airport.drop_duplicates(subset=['Airport Name'])
    print("Número de duplicados en 'Airport Name':", dim_departure_airport['Airport Name'].duplicated().sum())
    input("Presione Enter para continuar...")

    # Dimensión de Pasajeros (ya tiene ID único)
    dim_passenger = df[['Passenger ID', 'First Name', 'Last Name', 'Gender', 'Age', 'Nationality']].drop_duplicates().copy()

    # --- Creación de la Tabla de Hechos ---
    # Asignar los ID de las dimensiones utilizando map
    df['DepartureDateID']   = df['Departure Date'].map(dim_departure_date.set_index('Departure Date')['DepartureDateID'])
    df['ArrivalAirportID']  = df['Arrival Airport'].map(dim_arrival_airport.set_index('Arrival Airport')['ArrivalAirportID'])
    df['PilotID']           = df['Pilot Name'].map(dim_pilot.set_index('Pilot Name')['PilotID'])
    df['FlightStatusID']    = df['Flight Status'].map(dim_flight_status.set_index('Flight Status')['FlightStatusID'])
    df['DepartureAirportID'] = df['Airport Name'].map(dim_departure_airport.set_index('Airport Name')['DepartureAirportID'])

    # Crear la tabla de hechos con los campos requeridos
    fact_flight = df[['Passenger ID', 'DepartureDateID', 'ArrivalAirportID', 'PilotID', 'FlightStatusID', 'DepartureAirportID']].copy()

    # Mostrar dimensiones y hechos para verificación
    print("DimPassenger:")
    print(dim_passenger.head())
    print("Total registros:", len(dim_passenger))
    input("Presione Enter para continuar...")

    print("DimDepartureDate:")
    print(dim_departure_date.head())
    print("Total registros:", len(dim_departure_date))
    input("Presione Enter para continuar...")

    print("DimArrivalAirport:")
    print(dim_arrival_airport.head())
    print("Total registros:", len(dim_arrival_airport))
    input("Presione Enter para continuar...")

    print("DimPilot:")
    print(dim_pilot.head())
    print("Total registros:", len(dim_pilot))
    input("Presione Enter para continuar...")

    print("DimFlightStatus:")
    print(dim_flight_status.head())
    print("Total registros:", len(dim_flight_status))
    input("Presione Enter para continuar...")

    print("DimDepartureAirport:")
    print(dim_departure_airport.head())
    print("Total registros:", len(dim_departure_airport))
    input("Presione Enter para continuar...")

    print("FactFlight:")
    print(fact_flight.head())
    print("Total registros:", len(fact_flight))
    input("Presione Enter para continuar...")

    # Retornar todas las dimensiones y la tabla de hechos en una lista
    return [dim_passenger, dim_departure_date, dim_departure_airport, dim_arrival_airport, dim_pilot, dim_flight_status, fact_flight]
