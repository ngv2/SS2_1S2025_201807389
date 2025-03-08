import database
from tqdm import tqdm

def load(data):
    # Desempaquetamos las dimensiones y la tabla de hechos
    dim_passenger         = data[0]
    dim_departure_date    = data[1]
    dim_departure_airport = data[2]
    dim_arrival_airport   = data[3]
    dim_pilot             = data[4]
    dim_flight_status     = data[5]
    fact_flight           = data[6]

    try:
        # DIMENSION PASAJERO
        for _, row in tqdm(dim_passenger.iterrows(), total=len(dim_passenger), desc="Cargando datos de pasajeros"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimPassenger WHERE PassengerID = ?)
                BEGIN
                    INSERT INTO DimPassenger (PassengerID, FirstName, LastName, Gender, Age, Nationality)
                    VALUES (?, ?, ?, ?, ?, ?)
                END
            """, row['Passenger ID'], row['Passenger ID'], row['First Name'], row['Last Name'], row['Gender'], row['Age'], row['Nationality'])
        print("Datos de pasajeros insertados")
        
        # DIMENSION AEROPUERTO DE SALIDA
        for _, row in tqdm(dim_departure_airport.iterrows(), total=len(dim_departure_airport), desc="Cargando aeropuertos de salida"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimDepartureAirport WHERE DepartureAirportID = ?)
                BEGIN
                    INSERT INTO DimDepartureAirport (DepartureAirportID, AirportName, AirportCountryCode, CountryName, AirportContinent, Continents)
                    VALUES (?, ?, ?, ?, ?, ?)
                END
            """, row['DepartureAirportID'], row['DepartureAirportID'], row['Airport Name'], row['Airport Country Code'], row['Country Name'], row['Airport Continent'], row['Continents'])
        print("Datos de aeropuertos de salida insertados")
        
        # DIMENSION AEROPUERTO DE LLEGADA
        for _, row in tqdm(dim_arrival_airport.iterrows(), total=len(dim_arrival_airport), desc="Cargando aeropuertos de llegada"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimArrivalAirport WHERE ArrivalAirportID = ?)
                BEGIN
                    INSERT INTO DimArrivalAirport (ArrivalAirportID, AirportName)
                    VALUES (?, ?)
                END
            """, row['ArrivalAirportID'], row['ArrivalAirportID'], row['Arrival Airport'])
        print("Datos de aeropuertos de llegada insertados")
        
        # DIMENSION PILOTO
        for _, row in tqdm(dim_pilot.iterrows(), total=len(dim_pilot), desc="Cargando datos de pilotos"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimPilot WHERE PilotID = ?)
                BEGIN
                    INSERT INTO DimPilot (PilotID, PilotName)
                    VALUES (?, ?)
                END
            """, row['PilotID'], row['PilotID'], row['Pilot Name'])
        print("Datos de pilotos insertados")
        
        # DIMENSIÓN ESTADO DE VUELO
        for _, row in tqdm(dim_flight_status.iterrows(), total=len(dim_flight_status), desc="Cargando estados de vuelo"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimFlightStatus WHERE FlightStatusID = ?)
                BEGIN
                    INSERT INTO DimFlightStatus (FlightStatusID, FlightStatus)
                    VALUES (?, ?)
                END
            """, row['FlightStatusID'], row['FlightStatusID'], row['Flight Status'])
        print("Datos de estados de vuelo insertados")
        
        # DIMENSIÓN FECHA DE SALIDA
        for _, row in tqdm(dim_departure_date.iterrows(), total=len(dim_departure_date), desc="Cargando fechas de salida"):
            database.cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM DimDepartureDate WHERE DepartureDateID = ?)
                BEGIN
                    INSERT INTO DimDepartureDate (DepartureDateID, [Date], [Year], [Month], [Day])
                    VALUES (?, ?, ?, ?, ?)
                END
            """, row['DepartureDateID'], row['DepartureDateID'], row['Departure Date'], row['Year'], row['Month'], row['Day'])
        print("Datos de fechas de salida insertados")
        
        # TABLA DE HECHOS: Datos de vuelos
        for _, row in tqdm(fact_flight.iterrows(), total=len(fact_flight), desc="Cargando datos de vuelos"):
            database.cursor.execute("""
                INSERT INTO FactFlight (PassengerID, DepartureDateID, DepartureAirportID, ArrivalAirportID, PilotID, FlightStatusID)
                VALUES (?, ?, ?, ?, ?, ?)
            """, row['Passenger ID'], row['DepartureDateID'], row['DepartureAirportID'], row['ArrivalAirportID'], row['PilotID'], row['FlightStatusID'])
        print("Datos de vuelos insertados")
        
        # Confirmar las transacciones
        database.conn.commit()
        print("Datos cargados exitosamente.")
    
    except Exception as e:
        print("Error al insertar datos en la fila:")
        print(row)
        print(f"Error: {e}")
        database.conn.rollback()  # Retrocede en caso de error
    # Opcional: se puede cerrar la conexión si ya no se requiere más operaciones.
    # database.close_connection()