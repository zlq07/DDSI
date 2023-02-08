"""
    DDSI: PRÁCTICA 3
    
    GRUPO DE TRABAJO: A1_ddsimola:D
    MIEMBROS:
    - Luis Miguel Guirado Bautista
    - Pablo Irigoyen Cortadi
    - Linqi Zhu
    - Miguel Ángel Serrano Villena
"""

# encoding: utf-8
###############################################################################
import oracledb
from getpass import getpass
from sys import argv
import toml
import pandas as pd
###############################################################################
from sub1 import *
from sub2 import *
from sub3 import *
from sub4 import *
from insertar_tuplas import *
from crear_tablas import *
from crear_disparadores import *
from borrar_tablas import *


def inicializar_bd(conexion: oracledb.Connection):
    print('Creando tablas en la base de datos...\n')
    crear_tablas(conexion)
    print('Insertando tuplas predefinidas en la base de datos...\n')
    insertar_tuplas_tablas_sub1(conexion)
    insertar_tuplas_tablas_sub3(conexion)
    insertar_tuplas_tablas_sub4(conexion)
    print('Creando disparadores...\n')
    crear_disparadores(conexion)


###############################################################################

def main():
    """
    Uso del programa:

        - `py main.py`                          -> Datos por entrada estándar
        - `py main.py <nombre_archivo>.toml`    -> Datos por fichero TOML
        - `py main.py <usuario>`                -> Usuario por parámetros y contraseña por entrada estándar
        - `py main.py <usuario> <contraseña>`   -> Datos por argumentos
    """

    # * ---------- Obtenemos el usuario y la contraseña ----------

    username: str = None
    password: str = None

    # Si no le pasamos argumentos nos pide los datos de login por la entrada estándar
    if (len(argv) == 1):
        username = getpass('Usuario: ')

    # Si le pasamos uno:
    elif (len(argv) == 2):

        # Si es un fichero .toml, importa los datos de login desde ese archivo
        """
            Formato del archivo TOML:
            username = 'x0000000'
            password = 'x0000000'
        """
        if (argv[1].endswith('.toml')):
            try:
                params = toml.load(argv[1])
            except Exception as e:
                print(
                    f'Se pasó un fichero TOML, pero no pudo cargarse correctamente: \n {e}')
                exit()
            else:
                username, password = params['username'], params['password']

        # Si no, decide que es el nombre de usuario
        else:
            username = argv[1]

    # Si le pasamos 2, suponemos que son el usuario y la contraseña
    elif (len(argv) == 3):
        username, password = argv[1], argv[2]

    # Si no le pasamos una contraseña
    if (password == None):
        password = getpass('Contraseña: ')

    # * ---------- Establecemos la conexión ----------

    try:
        print('\nConectando a la base de datos...')
        conexion: oracledb.Connection = oracledb.connect(host='oracle0.ugr.es',
                                                         port='1521',
                                                         service_name='practbd.oracle0.ugr.es',
                                                         user=username,
                                                         password=password)
    except Exception as e:
        print(f'\n\tNo se ha podido establecer conexión con la base de datos: \n {e}')
        exit()
    else:
        print('\n\tConexión realizada correctamente.\n')

    # * ---------- Ahora podemos operar en la base de datos ----------

    try:
        inicializar_bd(conexion)
        OPCION_SALIR: int = 5
        opc: int = None
        while (opc != OPCION_SALIR):
            menu_principal()
            opc = escoger_opcion()
            match opc:
                case 1:
                    interfaz_gestion_mantenimiento_camiones_contenedores(conexion)
                case 2:
                    interfaz_gestion_rutas(conexion)
                case 3:
                    interfaz_localizacion_contenedores(conexion)
                case 4:
                    interfaz_gestion_planta(conexion)
                case _:
                    # Default:
                    print('\nEsta opción no existe.\n')
    except KeyboardInterrupt:
        print('\n\nCerrando conexión por interrupción del usuario...')
    finally:
        print('Cerrando conexión...')
        borrar_tablas(conexion)
        conexion.close()
        print("\nConexión cerrada.\n")

###############################################################################


if __name__ == "__main__":
    main()