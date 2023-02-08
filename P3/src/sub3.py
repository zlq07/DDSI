###############################################################################
############### SUBSISTEMA DE LOCALIZACIÓN DE CONTENEDORES ####################
###############################################################################

# -----------------------------------------------------------------------------
import oracledb
import pandas as pd
from funciones_comunes import *
# -----------------------------------------------------------------------------

def interfaz_localizacion_contenedores(conexion: oracledb.Connection):
    """
        Interfaz referente al subsistema de Localización de Contenedores.
        En esta interfaz se podrá escoger entre buscar un grupo de contenedores,
        mostrar un grupo de contenedores y guardar un trayecto hacia un grupo de 
        contenedores como favorito.
    """

    # FUNCIONES ENCAPSULADAS ------------------------------------------------------------------------------------------------

    def menu_localizacion_contenedores():
        """
            Imprime el menú de opciones del subsistema de Localización de Contenedores.
        """
        print('\n\t--- MENÚ PRINCIPAL LOCALIZACIÓN DE CONTENEDORES ---')
        print('\n\tOpciones:')
        print('\n\t1. Buscar grupo de contenedores.')
        print('\t2. Mostrar grupo de contenedores.')
        print('\t3. Calcular trayecto.')
        print('\t4. Olvidar trayecto.')
        print('\t5. Gestionar trayectos favoritos.')
        print('\t6. Salir.')

    def buscar_grupo_contenedores(id_gr_cont: str):
        """
            Busca un grupo de contenedores pasado como parámetro.
            Devuelve 'True' si se ha encontrado; 'False' en caso 
            contrario.
        """
        encontrado: bool = False

        # Realizar consulta sobre la base de datos:
        with conexion.cursor() as cursor:
            try:
                query = f'SELECT id_gr_cont FROM Grupo_contenedores WHERE (id_gr_cont = {id_gr_cont})'
                encontrado = cursor.execute(query).fetchone() != None
            except Exception as e:
                print(f'\nNo se ha podido realizar la consulta sobre la tabla Grupo_contenedores para buscarlo.\n {e}')

        return encontrado
    
    def mostrar_grupo_contenedores(id_gr_cont: str):
        """
            Muestra un grupo de contenedores pasado como parámetro.
        """
        # Realizar consulta sobre la base de datos:
        with conexion.cursor() as cursor:
            try:
                if (buscar_grupo_contenedores(id_gr_cont)):
                    try:
                        # Primero, obtenemos los nombres de las columnas de la tabla:
                        query: str = f'SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME=\'GRUPO_CONTENEDORES\''
                        columnas: list = cursor.execute(query).fetchall()

                        # Aparecerán tuplas de tamaño 1; nos quedamos solo con su contenido:
                        columnas = [t[0] for t in columnas]

                        # Después, construimos una tabla de Pandas (dataframe) con las tuplas obtenidas
                        # y los nombres de las columnas que hemos obtenidos anteriormente:
                        query = f'SELECT * FROM Grupo_contenedores WHERE (id_gr_cont = {id_gr_cont})'
                        dataframe: pd.DataFrame = pd.DataFrame(cursor.execute(
                                                                  query).fetchall(), columns=columnas)

                        # Mostramos la tabla:
                        if (not dataframe.empty):
                            print("\n\n")
                            print(dataframe.to_string(index=False))
                            print("\n")
                        else:
                            print('\nNo existen tuplas en esta tabla.\n')
                    except Exception as e:
                        print(f'\nHubo un error al intentar mostrar el grupo de contenedores {id_gr_cont}:\n {e}')
                else:
                    print(f'\nEl grupo de contenedores no existe.\n')
            except Exception as e:
                print(f'\nNo se ha podido realizar la consulta sobre la tabla Grupo_contenedores para mostrarlo.\n {e}')

    def calcular_trayecto(id_usr: str, id_tray: str):
        """
            Calcula un trayecto, vinculándolo con un usuario.
        """

        with conexion.cursor() as cursor:
            try:
                query = f'INSERT INTO Usa VALUES (\'{id_usr}\',\'{id_tray}\')'
                cursor.execute(query)
                print(f'\nSe ha calculado correctamente el trayecto {id_tray}.\n')
                cursor.execute("COMMIT")
            except Exception as e:
                print(f'\nNo se ha podido calcular correctamente el trayecto.\n {e}')

    def olvidar_trayecto(id_usr: str, id_tray: str):
        """
            Olvida un trayecto, desvinculándolo de un usuario.
        """

        with conexion.cursor() as cursor:
            try:
                query = f'DELETE FROM Usa WHERE (id_usuario = \'{id_usr}\') AND (id_trayecto = \'{id_tray}\')'
                cursor.execute(query)
                print(f'\nSe ha olvidado correctamente el trayecto {id_tray} para el usuario {id_usr}.\n')
                cursor.execute("COMMIT")
            except Exception as e:
                print(f'\nNo se ha podido olvidar correctamente el trayecto.\n {e}')     

    def gestionar_trayectos_favoritos():
        """
            Asignación/Desasignación de trayectos a/de usuarios.
        """

        # FUNCIONES ENCAPSULADAS ------------------------------------------------------------------------------------------------
        
        def menu_gestion_trayectos_favoritos():
            """
                Imprime el menú de opciones para gestionar los trayectos favoritos.
            """
            print('\n\t--- MENÚ GESTIÓN DE TRAYECTOS FAVORITOS ---')
            print('\n\tOpciones:')
            print('\n\t1. Guardar trayecto favorito.')
            print('\t2. Eliminar trayecto favorito.')
            print('\t3. Cancelar.')
            print('\t4. Terminar.')

        def guardar_trayecto_favorito(id_usr: str, id_tray: str):
            """
                Asigna un trayecto como favorito a un usuario.
            """

            # Realizar inserción sobre la tabla Usa, que vincula un usuario con un trayecto:
            with conexion.cursor() as cursor:
                try:
                    query = f'INSERT INTO Guarda_fav VALUES (\'{id_usr}\',\'{id_tray}\')'
                    cursor.execute(query)
                    print(f'\nSe ha asignado correctamente el trayecto {id_tray} como favorito del usuario {id_usr}.\n')
                except Exception as e:
                    print(f'\nNo se ha podido realizar la inserción sobre la tabla Guarda_fav.\n {e}')

        def eliminar_trayecto_favorito(id_usr: str, id_tray: str):
            """
                Desasigna un trayecto como favorito de un usuario.
            """

            # Realizar el borrado de la tupla sobre la tabla Usa, que vincula un usuario con un trayecto:
            with conexion.cursor() as cursor:
                try:
                    query = f'DELETE FROM Guarda_fav WHERE (id_usuario = \'{id_usr}\' and id_trayecto = \'{id_tray}\')'
                    cursor.execute(query)
                    print(f'\nSe ha desasignado correctamente el trayecto {id_tray} como favorito del usuario {id_usr}.\n')
                except Exception as e:
                    print(f'\nNo se ha podido realizar la eliminación de la tupla de la tabla Guarda_fav.\n {e}')

        def cancelar():
            """
                Deshace los cambios realizados sobre la asignación/desasignación de trayectos a usuarios.
            """
            print('\nDeshaciendo cambios...\n')
            with conexion.cursor() as cursor:
                try:
                    cursor.execute('ROLLBACK TO gestion_trayectos_favoritos')
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

        # ------------------------------------------------------------------------------------------------------------------

        conexion.cursor().execute('SAVEPOINT gestion_trayectos_favoritos') # Punto de guardado para la gestión de trayectos favoritos.

        OPCION_SALIR: int = 4
        opc: int = None

        while (opc != OPCION_SALIR):

            menu_gestion_trayectos_favoritos()
            opc = escoger_opcion()

            match opc:
                case 1:
                    # Guardar trayecto favorito:
                    id_usr: str  = input("\nIntroduzca el identificador del usuario: ")
                    id_tray: str = input("\nIntroduzca el identificador del trayecto: ")
                    guardar_trayecto_favorito(id_usr, id_tray)
                case 2:
                    # Eliminar trayecto favorito:
                    id_usr: str  = input("\nIntroduzca el identificador del usuario: ")
                    id_tray: str = input("\nIntroduzca el identificador del trayecto: ")
                    eliminar_trayecto_favorito(id_usr, id_tray)
                case 3:
                    # Cancelar
                    cancelar()
                case 4:
                    # Terminar:
                    terminar()
                case _: 
                    # Opción por defecto: no válida.
                    print('\nEsta opción no existe.\n')

    # ----------------------------------------------------------------------------------------------------------------------

    OPCION_SALIR: int = 6
    opc: int = None

    while (opc != OPCION_SALIR):

        menu_localizacion_contenedores()
        opc = escoger_opcion()

        match opc:
            case 1:
                # Buscar grupo de contenedores:
                id = str(input('\nIntroduzca el identificador del grupo de contenedores: '))
                if (buscar_grupo_contenedores(id)):
                    print("\nSe ha encontrado el grupo de contenedores.\n")
                else:
                    print("\nNo se ha encontrado el grupo de contenedores.\n")
            case 2:
                # Mostrar grupo de contenedores:
                id = str(input('\nIntroduzca el identificador del grupo de contenedores: '))
                mostrar_grupo_contenedores(id)
            case 3:
                # Calcular trayecto:
                id_usr = str(input('\nIntroduzca el identificador del usuario: '))
                id_tray = str(input('\nIntroduzca el identificador del trayecto: '))
                calcular_trayecto(id_usr, id_tray)
            case 4:
                # Olvidar trayecto:
                id_usr = str(input('\nIntroduzca el identificador del usuario: '))
                id_tray = str(input('\nIntroduzca el identificador del trayecto: '))
                olvidar_trayecto(id_usr, id_tray)
            case 5:
                # Gestionar trayectos favoritos: (asignar/desasignar trayectos a/de usuarios)
                gestionar_trayectos_favoritos()
            case 6:
                # Consolidar los cambios y salir al menú general:
                salir(conexion)
            case _: 
                # Opción por defecto: no válida.
                print('\nEsta opción no existe.\n')