###############################################################################
import oracledb
from getpass import getpass
###############################################################################

# Imprime un menu con las opciones
def menu():
    print('Opciones:')
    print('\t1. Borrado y nueva creación de las tablas e inserción de 10 tuplas predefinidas en el código en la tabla Stock')
    print('\t2. Dar de alta un pedido')
    print('\t3. Mostrar contenido de las tablas')
    print('\t4. Salir del programa y cerrar conexión')

# Le dice al usuario que escoja una opción de las existentes
def escoger_opcion() -> int:
    opc = 0
    while (opc < 1 or opc > 4):
        opc = int(input("Elija una opción: "))
    return opc 

###############################################################################

def main():

    # Datos del servidor
    host = 'oracle0.ugr.es'
    port = '1521'
    database = 'practbd.oracle0.ugr.es'
    
    # Obtenemos el usuario y la contraseña
    username: str = getpass("Usuario: ")
    password: str = getpass("Contraseña: ")

    # Establecemos la conexión
    try:
        print("Conectando a la base de datos...")
        conexion: oracledb.Connection = oracledb.connect(host=host,
                                                         port=port,
                                                         service_name=database,
                                                         user=username,
                                                         password=password)
    except:
        print('No se ha podido establecer conexión con la base de datos')
        exit()
    else:
        print('Conexión realizada correctamente')

    # Ahora podemos operar en la base de datos
    cursor: oracledb.Cursor = conexion.cursor()
    menu()
    opc = None
    while (opc != 4):
        opc = escoger_opcion()
        match opc:
            case 1:
                # Borrado y nueva creación de las tablas e inserción de 10 tuplas predefinidas en el código en la tabla Stock
                pass
            case 2:
                # Dar de alta un pedido
                pass
            case 3:
                # Mostrar el contenido de las tablas
                pass
            case 4:
                # Cerramos conexión con la base de datos
                print("Cerrando conexión...")
                conexion.close()
    
###############################################################################

if __name__ == "__main__":
    main()