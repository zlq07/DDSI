# SUBSISTEMA DE GESTIÓN DE RUTAS DE CAMIONES -------------------------------------------------------------------------------

import oracledb
from funciones_comunes import escoger_opcion, salir

# FUNCIONALIDAD PRIMERA


def asignar_parada_a_ruta(conexion: oracledb.Connection):
    """
        Añade una parada específica a una ruta específica
        Le pediremos al usuario que nos especifique el id. de una parada que no
        pertenezca a ninguna ruta más
        Después le especificamos el id. de una ruta.
    """
    ########################################################################################
    def consultar_contenedores_desasignados(conexion: oracledb.Connection) -> list:
        """
            Devuelve y muestra por pantalla los grupos de contenedores que no pertenecen a
            ninguna ruta
        """
        with conexion.cursor() as cursor:
            try:
                # Obtenemos todos los contenedores y les restamos los que estén ya en un grupo (tabla Contiene)
                query = 'SELECT id_gr_cont FROM Grupo_contenedores MINUS SELECT id_gr_cont FROM Contiene'
                tuplas = [t[0] for t in cursor.execute(query).fetchall()]
                for t in tuplas:
                    print(f'{t}')
                return tuplas
            except Exception as e:
                print(f'Ha ocurrido un error inesperado:\n{e}')
    ########################################################################################

    def mostrar_rutas(conexion: oracledb.Connection) -> list:
        """
            Devuelve y muestra por pantalla los ids. de rutas
        """
        with conexion.cursor() as cursor:
            try:
                query = "SELECT id_ruta FROM Ruta"
                rutas = [t[0] for t in cursor.execute(query).fetchall()]
                for r in rutas:
                    print(f'{r}')
                return rutas
            except Exception as e:
                print(f'Ha ocurrido un error inesperado:\n{e}')
    ########################################################################################

    def contenedor_asignado_a_ruta(conexion: oracledb.Connection, ruta: str, contenedor: str) -> bool:
        """
            Indica si un grupo de contenedores está asignado a una ruta
        """
        with conexion.cursor() as cursor:
            try:
                query = f"SELECT id_gr_cont, id_ruta FROM Contiene WHERE (id_gr_cont='{contenedor}' and id_ruta='{ruta}')"
                return (len(cursor.execute(query).fetchall()) != 0)
            except:
                print(f'Ha ocurrido un error inesperado:\n{e}')
    ########################################################################################
    # Imprimimos los id de contenedor por pantalla y le pedimos al usuario que introduzca uno de los ids
    disponibles: list = consultar_contenedores_desasignados(conexion)
    if (len(disponibles) == 0):
        print('No existen paradas disponibles, volviendo al menú...')
        return
    contenedor = str(input('Escriba el identificador de contenedor: '))
    if (contenedor not in disponibles):
        print('El contenedor especificado no se encuentra en la base de datos, volviendo al menú...')
        return
    # Imprimimos los id de ruta por pantalla y le pedimos al usuario que introduzca uno de los ids
    rutas = mostrar_rutas(conexion)
    ruta = str(input('Escriba el identificador de ruta: '))
    if (ruta not in rutas):
        print(
            'La ruta especificada no se encuentra en la base de datos, volviendo al menú...')
        return
    # Comprobamos que el contenedor no está ya asignado a la ruta
    if (contenedor_asignado_a_ruta(conexion, ruta, contenedor)):
        print('El contenedor ya pertenece a esta ruta, cancelando operación...\n')
        return

    with conexion.cursor() as cursor:
        cursor.execute('SAVEPOINT asignar_parada')
        try:
            # Asignamos el contenedor correspondiente a la ruta correspondiente
            print('Asignando grupo de contenedores a la ruta correspondiente...')
            query = f"INSERT INTO Contiene VALUES ('{contenedor}','{ruta}')"
            cursor.execute(query)
        except Exception as e:
            print(f'Ha ocurrido un error al asignar la parada a la ruta:\n{e}')
            cursor.execute('ROLLBACK TO asignar_parada')
        else:
            print(f'Contenedor {contenedor} asignado a ruta {ruta}\n')

# FUNCIONALIDAD SEGUNDA


def cambiar_ruta_incidencia(conexion: oracledb.Connection):
    """
        Se le especificará al usuario 2 ids. de camiones:
        - Primero el del camión reemplazado
        - Y segundo el del camión sustituto

        El camión reemplazado pasará a estar libre
        Si el camión sustituto está libre:
        - Este pasará a hacer la ruta del camión reemplazado
        Si el camión sustituto está ocupado
        - Este pasará a hacer la ruta del camión reemplazado además de la suya propia
    """
    ########################################################################################
    def mostrar_camiones_activos(conexion: oracledb.Connection) -> list:
        with conexion.cursor() as cursor:
            try:
                query = 'SELECT id_camion FROM Camion INTERSECT SELECT id_camion FROM Recorre'
                camiones = [t[0] for t in cursor.execute(query).fetchall()]
                print('Camiones asignados a una ruta:')
                for c in camiones:
                    print(c)
                return camiones
            except Exception as e:
                print(f'Ha ocurrido un error inesperado:\n{e}')
    ########################################################################################

    def get_camiones(conexion: oracledb.Connection):
        with conexion.cursor() as cursor:
            try:
                query = 'SELECT id_camion FROM Camion'
                camiones = [t[0] for t in cursor.execute(query).fetchall()]
                print('Camiones registrados: ')
                for c in camiones:
                    print(c)
                return camiones
            except Exception as e:
                print(f'Ha ocurrido un error inesperado:\n{e}')
    ########################################################################################
    # Le pedimos al usuario los camiones que desea reemplazar
    activos: list = mostrar_camiones_activos(conexion)
    if (len(activos) == 0):
        print('No existen camiones activos')
        return
    c1 = int(input('Escriba el id. del camión que debe ser reemplazado: '))
    if (c1 not in activos):
        print('El camión introducido no existe, volviendo al menú...')
        return

    camiones: list = get_camiones(conexion)
    c2 = int(input('Escriba el id. del camión que lo reemplazará: '))
    if (c2 not in camiones):
        print('El camión introducido no existe, volviendo al menú...')
        return

    if (c1 == c2):
        print("Los identificadores de camión coinciden, volviendo al menú...")
        return

    with conexion.cursor() as cursor:
        query = f"SELECT * FROM Recorre WHERE (id_camion='{c1}' or id_camion='{c2}')"
        datos = cursor.execute(query).fetchall()
        cursor.execute('SAVEPOINT cambiar_ruta')
        try:
            if (len(datos) == 1):
                # datos[] -> tupla
                # datos[][] -> columna (en este caso: id_ruta)
                r = datos[0][0]
                cursor.execute(
                    f"DELETE FROM Recorre WHERE (id_ruta='{r}' and id_camion='{c1}')")
                cursor.execute(f"INSERT INTO Recorre VALUES ('{r}', '{c2}')")
            elif (len(datos) == 2):  # Intercambiamos las rutas que realizan los camiones
                if (datos[0][0] == datos[-1][0]):
                    print(
                        'Los dos camiones realizan la misma ruta, volviendo al menú...')
                    return
                if (datos[0][1] == c1):  # La primera ruta pertenece al primer camión
                    r1 = datos[0][0]
                elif (datos[0][1] == c2):  # La primera ruta pertenece al segundo camión
                    r1 = datos[-1][0]
                cursor.execute(
                    f"DELETE FROM Recorre WHERE (id_camion='{c1}' and id_ruta='{r1}')")
                cursor.execute(f"INSERT INTO Recorre VALUES ('{r1}', '{c2}')")
        except Exception as e:
            print(f'Ha ocurrido un error:\n{e}')
            cursor.execute('ROLLBACK TO cambiar_ruta')
        else:
            print(
                f'El camión {c1} ha reemplazado al camión {c2} correctamente\n')

# FUNCIONALIDAD TERCERA


def eliminar_parada_ruta(conexion: oracledb.Connection):
    """
        Elimina una parada de una ruta específica
        Se le especificará al usuario un id. de ruta y un id. de
        grupo de contenedor
    """
    ########################################################################################
    def rutas_no_vacias(conexion: oracledb.Connection) -> list:
        """
            Devuelve y muestra por pantalla las rutas que tienen
            al menos una entrada en la tabla Contiene
        """
        with conexion.cursor() as cursor:
            try:
                query = f'SELECT id_ruta FROM Ruta INTERSECT SELECT id_ruta FROM Contiene'
                rutas = [t[0] for t in cursor.execute(query).fetchall()]
                print('Rutas con paradas:')
                for r in rutas:
                    print(r)
                return rutas
            except Exception as e:
                print(f'Ha ocurrido un error inesperado: \n{e}')
    ########################################################################################

    def mostrar_paradas_ruta(conexion: oracledb.Connection, ruta: str) -> list:
        """
            Devuelve y muestra por pantalla las paradas de una ruta
        """
        with conexion.cursor() as cursor:
            try:
                query = f"SELECT id_gr_cont FROM Contiene WHERE id_ruta='{ruta}'"
                paradas = [t[0] for t in cursor.execute(query).fetchall()]
                print(f'Paradas de la ruta {ruta}:')
                for p in paradas:
                    print(p)
                return paradas
            except Exception as e:
                print(f'Ha ocurrido un error inesperado: \n{e}')
    ########################################################################################

    # Pedimos la ruta al usuario y después consultamos sus paradas
    rutas: list = rutas_no_vacias(conexion)
    ruta = str(input('Escribe el id. de la ruta: '))
    if (ruta not in rutas):
        print('La ruta especificada no existe o está vacía, volviendo al menú')
        return
    # Le pedimos al usuario que introduzca una de las paradas
    paradas = mostrar_paradas_ruta(conexion, ruta)
    parada = str(input('Escribe el id. de la parada que desea eliminar: '))
    if (parada not in paradas):
        print('La parada especificada no se encuentra en la ruta')
        return

    with conexion.cursor() as cursor:
        cursor.execute('SAVEPOINT borrar_parada_ruta')
        try:
            # Operamos sobre la base de datos
            print('Borrando parada...')
            query = f'DELETE FROM Contiene WHERE (id_ruta={ruta} and id_gr_cont={parada})'
            cursor.execute(query)
        except Exception as e:
            print(f'Ha ocurrido un error: \n{e}')
            cursor.execute('ROLLBACK TO borrar_parada_ruta')
        else:
            print(
                f'La parada {parada} se ha eliminado correctamente de la ruta {ruta}')


def menu_subsistema2():
    """
        Imprime el menú principal del subsistema por pantalla
    """
    print('\n\t--- MENÚ DE GESTION DE RUTAS DE CAMIONES ---')
    print('\n\tOpciones:')
    print('\t1. Asignar parada a ruta')
    print('\t2. Cambiar ruta por incidencia')
    print('\t3. Eliminar parada de ruta')
    print('\t4. Cancelar cambios y salir')
    print('\t5. Confirmar cambios y salir')


def interfaz_gestion_rutas(conexion: oracledb.Connection):
    """
        Función principal del subsistema 2
    """
    conexion.cursor().execute('SAVEPOINT menu_sub2')
    opc = None
    while opc not in [4, 5]:
        menu_subsistema2()
        opc = escoger_opcion()
        match opc:
            case 1:
                asignar_parada_a_ruta(conexion)
            case 2:
                cambiar_ruta_incidencia(conexion)
            case 3:
                eliminar_parada_ruta(conexion)
            case 4:
                conexion.cursor().execute('ROLLBACK TO menu_sub2')
            case 5:
                salir(conexion)
            case _:
                print('Opcion no valida')
