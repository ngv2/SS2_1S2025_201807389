
from extract import extract
from transform import transform
from load import load

def main ():
    print ("Hello World!")
    print("\033[H\033[J")
    while True:
            print("\033[H\033[J")
            print("Seleccione una opción:")
            print("1. Borrar Modelo")
            print("2. Crear Modelo")
            print("3. Extraer datos")
            print("4. Transformar datos")
            print("5. Cargar datos")
            print("6. Realizar Consultas")
            print("7. Salir")
            # C:\Users\Randall\Documents\U\Pract. Finales\Semi2\Repo Lab\semi2Lab\clasePractica1\VuelosDataSet.csv
            option = input("Opción: ")

            if option == "1":
                print("Borrando tablas...")
                # Aquí iría el código para borrar el modelo
                input("Presione Enter para continuar...")
            elif option == "2":
                print("Creando tablas...")
                # Aquí iría el código para crear el modelo (ejecutar scripts SQL, etc.)
                input("Presione Enter para continuar...")
            elif option == "3":
                df = extract()
                if df is not None:
                    print("Datos extraídos correctamente.")
                else:
                    print("No se pudo extraer la información.")
                input("Presione Enter para continuar...")

            elif option == "4":
                if df is None:
                    print("Primero debes extraer los datos (opción 3).")
                else:
                    transformed_data = transform(df)
                    print("Datos transformados correctamente.")
                input("Presione Enter para continuar...")
            elif option == "5":
                if transformed_data is None:
                    print("Primero debes transformar los datos (opción 4).")
                else:
                    load(transformed_data)
                input("Presione Enter para continuar...")
            elif option == "6":
                print("Realizando consultas...")
            elif option == "7":
                print("Saliendo...")
                break
            else:
                print("Opción inválida")
                input("Presione Enter para continuar...")
                print("\033[H\033[J")


if __name__ == "__main__":
    main()  