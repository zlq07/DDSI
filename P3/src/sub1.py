#SUBSISTEMA DE GESTION Y MANTENIMIENTO DE CAMNIONES Y CONTENEDORES
import oracledb
import pandas as pd
from funciones_comunes import escoger_opcion, salir

def interfaz_gestion_mantenimiento_camiones_contenedores(conexion: oracledb.Connection):
    """
        Interfaz referente al subsistema de Gestion y mantenimiento de camiones y contenedores.
        En esta interfaz se podrá escoger entre buscar sin un contenedor se encuentra en mantenimiento y si es así, que tipo de mantenimiento,
        mostrar los contenedores que se encuentren en mantenimiento e iniciar un mantenimiento.
    """

    # FUNCIONES ENCAPSULADAS ------------------------------------------------------------------------------------------------

    def menu_gestion_mantenimiento_camiones_contenedores():
        """
            Imprime el menú de opciones del subsistema de Gestión y Mantenimiento de camiones y contenedores.
        """
        print('\n\t- MENÚ PRINCIPAL GESTION Y MANTENIMIENTO DE CAMNIONES Y CONTENEDORES -')
        print('\n\tOpciones:')
        print('\n\t1. Mostrar contenedores en mantenimiento.')
        print('\t2. Buscar si contenedor se encuentra en Revision o Reparacion.')
        print('\t3. Iniciar un mantenimiento de un contenedor.')
        print('\t4. Finalizar un mantenimiento de un contenedor.')
        print('\t5. Mostrar historial de los contenedores en mantenimiento.')
        print('\t6. Salir.')

    def buscar_contenedor_mantenimiento():
        """
            Busca un contenedor pasado como parámetro.
            Devuelve '0' si se ha encontrado y es una revisión; '1' en caso 
            de ser una reparacion: "-1" en caso de no encontrarlo.
        """
        # Realizar consulta sobre la base de datos:
        with conexion.cursor() as cursor:
            try:
                tipo_mantenimiento = -1
                id_contenedor = int(input("\nInserte id de contenedor a buscar: "))

                try:
                    query = f'SELECT TIPO_MANTENIMIENTO FROM MANTENIMIENTO WHERE (ID_CONTENEDOR = {id_contenedor})'
                    tipo_mantenimiento_encontrado = cursor.execute(query).fetchone() != None
                except Exception as e:
                    print(f'\nNo se ha podido comprobar el Id de contenedor sobre la tabla MANTENIMIENTO.\n {e}')

                if(tipo_mantenimiento_encontrado):
                    tipo_mantenimiento = cursor.execute(query).fetchone()

                    if (tipo_mantenimiento == (0,)):
                        print("El contenedor se encuentra en Revisión.\n")
                    if (tipo_mantenimiento == (1,)):
                        print("El contenedor se encuentra en Reparación.\n")
                else:
                    print("El contenedor no se encuentra en Mantenimiento.\n")

            except Exception as e:
                print(f'\nNo se ha podido realizar la consulta sobre la tabla MANTENIMIENTO para buscarlo.\n {e}')

    def mostrar_tabla(tabla: str):
        """
            Muestra los contenedores en mantenimiento.
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
                print(f'Hubo un error al intentar mostrar la tabla {tabla}:\n {e}')

    def iniciar_mantenimiento():
        """
            Inicia un mantenimiento a un contenedor.
        """
        with conexion.cursor() as cursor:
            try:
                id_mantenimiento = int(input("\nInserte id de mantenimiento: "))

                try:
                    query = f'SELECT ID_MANTENIMIENTO FROM MANTENIMIENTO WHERE (ID_MANTENIMIENTO = {id_mantenimiento})'
                    id_mantenimiento_encontrado = cursor.execute(query).fetchone() != None
                except Exception as e:
                    print(f'\nNo se ha podido comprobar el Id de mantenimiento sobre la tabla MANTENIMIENTO.\n {e}')

                if(id_mantenimiento_encontrado):
                    while(id_mantenimiento_encontrado):
                        print('\nEste Id de mantenimiento ya se encuentra en uso:\n')
                        id_mantenimiento = int(input("\nInserte id de mantenimiento: "))
                        try:
                            query = f'SELECT ID_MANTENIMIENTO FROM MANTENIMIENTO WHERE (ID_MANTENIMIENTO = {id_mantenimiento})'
                            id_mantenimiento_encontrado = cursor.execute(query).fetchone() != None
                        except Exception as e:
                            print(f'\nNo se ha podido comprobar el Id de mantenimiento sobre la tabla MANTENIMIENTO.\n {e}')

                id_trabajador = int(input("\nInserte id de trabajador: "))

                id_contenedor = int(input("\nInserte id de contenedor: "))

                try:
                    query = f'SELECT ID_CONTENEDOR FROM MANTENIMIENTO WHERE (ID_CONTENEDOR = {id_contenedor})'
                    id_contenedor_encontrado = cursor.execute(query).fetchone() != None
                except Exception as e:
                    print(f'\nNo se ha podido comprobar el Id de contenedor sobre la tabla MANTENIMIENTO.\n {e}')
                
                if(id_contenedor_encontrado):
                    while(id_contenedor_encontrado):
                        print('\nEste Id de contenedor ya se encuentra en uso:\n')
                        id_contenedor = int(input("\nInserte id de contenedor: "))
                        try:
                            query = f'SELECT ID_CONTENEDOR FROM MANTENIMIENTO WHERE (ID_CONTENEDOR = {id_contenedor})'
                            id_contenedor_encontrado = cursor.execute(query).fetchone() != None
                        except Exception as e:
                            print(f'\nNo se ha podido comprobar el Id de contenedor sobre la tabla MANTENIMIENTO.\n {e}')
                
                tipo_mantenimiento = int(input("\nInserte tipo de mantenimiento (0 -> Revision, 1 -> Reparacion): "))

                while(tipo_mantenimiento < 0 or tipo_mantenimiento > 1):
                        print('\nEste Tipo de Mantenimiento no existe:\n')
                        tipo_mantenimiento = int(input("\nInserte tipo de mantenimiento (0 -> Revision, 1 -> Reparacion): "))

                query = f"INSERT INTO MANTENIMIENTO VALUES ({id_mantenimiento}, {id_trabajador}, {id_contenedor}, {tipo_mantenimiento})"
                conexion.cursor().execute(query)
            except Exception as e:
                print(f'\nNo se ha podido realizar la inserción sobre la tabla MANTENIMIENTO.\n {e}')
            else:
                print('\nMantenimiento iniciado con éxito.\n')

    def finalizar_mantenimiento():
        """
            Finaliza un mantenimiento a un contenedor.
        """
        result = 0

        with conexion.cursor() as cursor:
            try:
                result: int = 0

                id_mantenimiento = int(input("\nInserte id de mantenimiento: "))
                query = f'SELECT ID_MANTENIMIENTO FROM MANTENIMIENTO WHERE (ID_MANTENIMIENTO = {id_mantenimiento})'
                id_mantenimiento_encontrado = cursor.execute(query).fetchone() != None

                if(id_mantenimiento_encontrado):
                    query = f"DELETE FROM MANTENIMIENTO WHERE (ID_MANTENIMIENTO = {id_mantenimiento})"
                    conexion.cursor().execute(query)
                    result = 1
                else:
                    print(f'\nEste Id de mantenimiento no se ha encontrado.')

            except Exception as e:
                print(f'\nNo se ha podido realizar la actualización sobre la tabla MANTENIMIENTO.\n {e}')
            else:
                if(result == 1):
                    print('\nMantenimiento actualizado con éxito.\n')
                    cursor.execute("COMMIT")
                else:
                    print('\nNo se pudo actualizar el mantenimiento.\n')

    # ----------------------------------------------------------------------------------------------------------------------

    OPCION_SALIR: int = 6
    opc: int = None

    while (opc != OPCION_SALIR):

        menu_gestion_mantenimiento_camiones_contenedores()
        opc = escoger_opcion()

        match opc:
            case 1:
                mostrar_tabla('MANTENIMIENTO')
            case 2:
                buscar_contenedor_mantenimiento()
            case 3:
                iniciar_mantenimiento()
            case 4:
                finalizar_mantenimiento()
            case 5:
                mostrar_tabla('HISTORIAL_MANTENIMIENTO')
            case 6:
                salir(conexion)
            case _: 
                print('\nEsta opción no existe.\n')