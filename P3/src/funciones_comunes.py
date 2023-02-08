
import oracledb

def menu_principal():
    """
        Imprime el menú principal por pantalla
    """
    print('\n\t--- MENÚ PRINCIPAL ---')
    print('\n\tOpciones:\n')
    print('\t1. Menú Subsistema Gestion y Mantenimiento de Contenedores y Camiones.')
    print('\t2. Menú Subsistema de Gestión de Rutas de Camiones.')
    print('\t3. Menú Subsistema Localización de Contenedores.')
    print('\t4. Menú Subsistema Gestion de planta.')
    print('\t5. Salir del programa y cerrar conexión.')
    print('\n\t- Pulsar CTRL+C para interrumpir el programa y borrar toda la base da datos -')

def escoger_opcion() -> int:
    """
        Solicita un número por entrada estándar
    """
    try:
        opc: int = int(input("\nElija una opción: "))
    except ValueError:
        print('Debe introducir un número')
        opc = -1
    return opc

def salir(conexion: oracledb.Connection):
    """
        Consolida los cambios realizados anteriormente en la BD antes de salir.
    """
    conexion.cursor().execute("COMMIT")