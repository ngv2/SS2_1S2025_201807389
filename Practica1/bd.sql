-- Crear la base de datos
CREATE DATABASE FlightDataWarehouse;
GO

-- Seleccionar la base de datos
USE FlightDataWarehouse;
GO

-- Crear la tabla de dimensión para Pasajeros (PassengerID ahora es NVARCHAR)
CREATE TABLE DimPassenger (
    PassengerID NVARCHAR(50) PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Gender NVARCHAR(10),
    Age INT,
    Nationality NVARCHAR(50)
);
GO

-- Crear la tabla de dimensión para Fechas de Salida
CREATE TABLE DimDepartureDate (
    DepartureDateID INT PRIMARY KEY,
    [Date] DATE,
    [Year] INT,
    [Month] INT,
    [Day] INT
);
GO

-- Crear la tabla de dimensión para Aeropuerto de Salida
CREATE TABLE DimDepartureAirport (
    DepartureAirportID INT PRIMARY KEY,
    AirportName NVARCHAR(100),
    AirportCountryCode NVARCHAR(10),
    CountryName NVARCHAR(50),
    AirportContinent NVARCHAR(50),
    Continents NVARCHAR(50)
);
GO

-- Crear la tabla de dimensión para Aeropuerto de Llegada
CREATE TABLE DimArrivalAirport (
    ArrivalAirportID INT PRIMARY KEY,
    AirportName NVARCHAR(100)
);
GO

-- Crear la tabla de dimensión para Pilotos
CREATE TABLE DimPilot (
    PilotID INT PRIMARY KEY,
    PilotName NVARCHAR(100)
);
GO

-- Crear la tabla de dimensión para Estado del Vuelo
CREATE TABLE DimFlightStatus (
    FlightStatusID INT PRIMARY KEY,
    FlightStatus NVARCHAR(50)
);
GO

-- Crear la tabla de hechos: FactFlight
-- FactID es auto-incrementable y PassengerID es NVARCHAR para admitir valores alfanuméricos.
CREATE TABLE FactFlight (
    FactID INT IDENTITY(1,1) PRIMARY KEY,
    PassengerID NVARCHAR(50),
    DepartureDateID INT,
    DepartureAirportID INT,
    ArrivalAirportID INT,
    PilotID INT,
    FlightStatusID INT,
    CONSTRAINT FK_FactFlight_Passenger FOREIGN KEY (PassengerID) 
        REFERENCES DimPassenger(PassengerID),
    CONSTRAINT FK_FactFlight_DepartureDate FOREIGN KEY (DepartureDateID) 
        REFERENCES DimDepartureDate(DepartureDateID),
    CONSTRAINT FK_FactFlight_DepartureAirport FOREIGN KEY (DepartureAirportID) 
        REFERENCES DimDepartureAirport(DepartureAirportID),
    CONSTRAINT FK_FactFlight_ArrivalAirport FOREIGN KEY (ArrivalAirportID) 
        REFERENCES DimArrivalAirport(ArrivalAirportID),
    CONSTRAINT FK_FactFlight_Pilot FOREIGN KEY (PilotID) 
        REFERENCES DimPilot(PilotID),
    CONSTRAINT FK_FactFlight_FlightStatus FOREIGN KEY (FlightStatusID) 
        REFERENCES DimFlightStatus(FlightStatusID)
);
GO