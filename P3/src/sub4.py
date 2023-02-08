###############################################################################
############### SUBSISTEMA DE GESTION DE LA PLANTA ####################
###############################################################################

# -----------------------------------------------------------------------------
import oracledb
import pandas as pd
from funciones_comunes import escoger_opcion
# -----------------------------------------------------------------------------

def interfaz_gestion_planta(conexion: oracledb.Connection):

    def menu_gestion_planta():
        print('\n\t--- MENÚ PRINCIPAL Gestion de planta ---')
        print('\n\tOpciones:')
        print('\n\t1. Crear nuevos de envios.')
        print('\t2. Asignar envios.')
        print('\t3. Registro de peso y horas.')
        print('\t4. Modificar tipo de residuo del envio')
        print('\t5. Cancelar.')
        print('\t6. Terminar.')

    def mostrar_tabla(tabla: str):
        """
            Muestra la tabla con nombre `tabla`
        """
        print(f'\n\n\t---Tabla {tabla}---\n\t')
        with conexion.cursor() as cursor:
            try:
                # Primero obtenemos los nombres de las columnas de la tabla
                columnas: list = cursor.execute(
                    f'SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME=\'{tabla.upper()}\'').fetchall()

                # Apareceran tuplas de tamaño 1, nos quedamos solo con su contenido
                columnas = [t[0] for t in columnas]

                # Despues construimos una tabla de Pandas (dataframe) con las tuplas obtenidas
                # y los nombres de columnas que hemos obtenidos anteriormente
                dataframe: pd.DataFrame = pd.DataFrame(cursor.execute(
                    f'SELECT * FROM {tabla}').fetchall(), columns=columnas)

                # Mostramos la tabla
                if (not dataframe.empty):
                    print(dataframe.to_string(index=False))
                else:
                    print('No existen tuplas en esta tabla.')

            except Exception as e:
                print(
                    f'Hubo un error al intentar mostrar la tabla {tabla}:\n {e}')

    def crear_envio():
        
        mostrar_tabla('Envio')
        id_envio = int(input('\nIntroduzca el id de envio: '))
        tipo_residuo = int(input("\nInserte Tipo de residuo\n1: orgánico \n2:papel/cartón \n3: vidrio\n4: pilas\n5:electrodomésticos\n6: ropa\n : "))

        print("\nCreando el envio...")
        with conexion.cursor() as cursor:
            cursor.execute('SAVEPOINT modifica_envio')
            try:
                query = f"INSERT INTO Envio VALUES ({id_envio},{tipo_residuo})"
                cursor.execute(query)
            except Exception as e:
                print(f'\nNo se ha podido procesar el envio:\n {e}')
                cursor.execute('ROLLBACK TO modifica_envio')
            else:
                print('\n\tEl envio se ha procesado correctamente.')
                mostrar_tabla('Envio')
    
    def asignar_envio():
        id_envio: int = 0
        id_gestor: int = 0
        id_camion: int = 0

        with conexion.cursor() as cursor:
            try:
                mostrar_tabla('Gestor')
                id_gestor = int(input("\nInserte código de id gestor: "))
                query = f'SELECT ID_GESTOR FROM Gestor WHERE ID_GESTOR={id_gestor}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl gestor se ha procesado correctamente.')
            
            try:
                mostrar_tabla('Envio')
                id_envio = int(input("\nInserte código de id envio: "))
                query = f'SELECT ID_ENVIO FROM Envio WHERE ID_ENVIO={id_envio}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl envio se ha procesado correctamente.')
                
            try:
                mostrar_tabla('Camion')
                id_camion = int(input("\nInserte código de id camion : "))
                query = f'SELECT ID_CAMION FROM Camion WHERE ID_CAMION={id_camion}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl camion se ha procesado correctamente.')
            
            try:
                query = f'INSERT INTO Asigna VALUES ({id_gestor}, {id_envio}, {id_camion})'
                cursor.execute(query)
            except Exception as e:
                print(f'\nNo se ha podido insertar el detalle del pedido:\n {e}')
            else:
                print('\n\tEl Asinacion se ha procesado correctamente.')
                mostrar_tabla('Asigna')

    def registro_peso():
        id_servicio: int = 0
        id_camion: int = 0

        with conexion.cursor() as cursor:
            try:
                mostrar_tabla('Planta_reciclaje')
                id_servicio = int(input("\nInserte código de id servicio: "))
                query = f'SELECT ID_SERVICIO FROM Planta_reciclaje WHERE ID_SERVICIO={id_servicio}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl servicio se ha procesado correctamente.')
            
            try:
                mostrar_tabla('Camion')
                id_camion = int(input("\nInserte código de id camion : ")) 
                query = f'SELECT ID_CAMION FROM Camion WHERE ID_CAMION={id_camion}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl camion se ha procesado correctamente.')
            
            peso_salida = int(input('\nIntroduzca el peso salida: '))
            peso_entrada = int(input('\nIntroduzca el peso entrada: '))
            fechayhora_salida = (input('Introducir el dia y la hora de la salida YYYY-MM-DD HH:MI:'))
            fechayhora_entrada = (input('Introducir el dia y la hora de la entradaYYYY-MM-DD HH:MI:'))
           
            try:
                query = f"INSERT INTO Peso_hora_supone VALUES ({id_servicio},{id_camion},{peso_salida},{peso_entrada},TO_DATE('{fechayhora_salida}:00','YYYY-MM-DD HH24:MI:SS'), TO_DATE('{fechayhora_entrada}:00','YYYY-MM-DD HH24:MI:SS'))"
                cursor.execute(query)
            except Exception as e:
                print(f'No se pueden insertar las tuplas:\n {e}')
            else:
                print('Se han insertado las tuplas correctamente.')
                mostrar_tabla('Peso_hora_supone')
    
    def modificar_envio():
        with conexion.cursor() as cursor:
            try:
                mostrar_tabla('Envio')
                mostrar_tabla('Asigna')
                id_envio = int(input("\nInserte código de id de envio que desea modificar : ")) 
                tipo_residuo = int(input("\nInserte Tipo de residuo\n1: orgánico \n2:papel/cartón \n3: vidrio\n4: pilas\n5:electrodomésticos\n6: ropa\n : "))
                query = f'UPDATE Envio Set TIPO_RESIDUO={tipo_residuo} WHERE ID_ENVIO={id_envio}'
                cursor.execute(query)
            except Exception as e:
                print(f'Ha ocurrido un error en la base de datos:\n {e}')
            else:
                print('\n\tEl envio se ha cambiado correctamente.')
                mostrar_tabla('Envio')
    
    def cancelar():
        print('\nDeshaciendo cambios...\n')
        with conexion.cursor() as cursor:
            try:
                cursor.execute('ROLLBACK TO gestion_planta')
            except:
                print('\nError al deshacer los cambios.\n')
            else:
                print('\nLos cambios se han deshecho correctamente.\n')

    def terminar():
        """
            Consolida los cambios realizados sobre la BD.
        """
        print("\nConsolidando cambios...\n")
        conexion.cursor().execute("COMMIT")     
        
    conexion.cursor().execute('SAVEPOINT gestion_planta') # Punto de guardado para la gestión de planta.
    OPCION_SALIR: int = 6
    opc: int = None

    while (opc != OPCION_SALIR):
        menu_gestion_planta()
        opc = escoger_opcion()

        match opc:
            case 1:
                crear_envio()
            case 2:
                asignar_envio()
            case 3:
                registro_peso()
            case 4:
                modificar_envio()
            case 5:
                    # Cancelar
                cancelar()
            case 6:
            # Terminar:
                terminar()
            case _: 
                # Opción por defecto: no válida.
                print('\nEsta opción no existe.\n')
  