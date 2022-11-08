# encoding: utf-8
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
def escoger_opcion(min: int, max: int) -> int:
    opc = 0
    while (opc < min or opc > max):
        opc = int(input("Elija una opción: "))
    return opc

# TODO
def ejecutar_sql():
    pass

def crear_tablas(cursor: oracledb.cursor.Cursor):
    try:
        filepath: str = '../crear_tablas.sql'
        cursor.execute('START {}'.format(filepath))
    except Exception as e:
        print('No se pueden crear las tablas \n {}'.format(e))
    else:
        print('Se han creado las tablas correctamente')

def insertar_tuplas_tabla_stock(cursor: oracledb.cursor.Cursor):
    try:
        filepath: str = '../insercion_tuplasPredefinidas_Stock.sql'
        cursor.execute('START {}'.format(filepath))
    except Exception as e:
        print('No se pueden insertar las tuplas en Stock: \n {}'.format(e))
    else:
        print('Se han creado las tablas correctamente')

def borrar_tabla(cursor, tabla: str):
    try:
        cursor.execute('DROP TABLE {tabla};'.format(tabla))
    except Exception as e:
        print('No se han podido borrar las tabla {} \n {}'.format(tabla, e))
    else:
        print('Tabla {} borrada correctamente'.format(tabla))

def alta_pedido(cursor: oracledb.cursor.Cursor):
    def menu_pedido():
        print('Opciones:')
        print('1. Añadir los detalles del pedido')
        print('2. Eliminar todos los detalles del pedido')
        print('3. Cancelar')
        print('4. Terminar')

    def aniadir_detalle():
        """
            Pedir cproducto
            Si existe y hay cantidad, se pide la cantidad
            si cantidad_pedido <= cantidad_db -> terminar
            sino dcirle que lo vuelva a intentar
        """
        codigo_producto: str = input("Inserte código de producto: ")
        cantidad_db = 0
        cantidad_cliente = 0
        try:
            query = f'SELECT Cantidad FROM Stock WHERE Cproducto={codigo_producto}'
            for row in cursor.execute(query):
                cantidad_db = row[0]
        except Exception as e:
            print(e)

        # Si la cantidad supera el maximo permitido o es cero o negativa volvemos a pedir cantidad
        while (cantidad_cliente > cantidad_db or cantidad_cliente <= 0):
            cantidad_cliente: int = int(input('Cantidad: '))


    def eliminar_detalle():
        """
            Eliminar todos los detalles SOLO en detalle-pedido
        """
        pass
    def cancelar():
        """
            borrar tupla de pedido y salir
        """
        pass
    def terminar():
        """
            terminar y salir
        """

    # Crear pedido

    menu_pedido()
    opc = None
    # Mientras no se cancele o se termine el pedido
    while (opc not in [3, 4]):
        opc = escoger_opcion(1,4)
        match opc:
            case 1:
                aniadir_detalle()
            case 2:
                eliminar_detalle()
            case 3:
                cancelar()
            case 4:
                terminar()
        if (opc != 4): 
            # Mostrar todas las tablas
            pass

def mostrar_tablas(cursor):
    # Insertar datos basicos del pedido -> INSERT INTO Pedido;

    # Menu detalles pedido (si opc no existe )

    pass
    

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
    cursor = conexion.cursor()
    menu()
    opc = None
    while (opc != 4):
        opc = escoger_opcion(1,4)
        match opc:
            case 1:
                # Borrado y nueva creación de las tablas e inserción de 10 tuplas predefinidas en el código en la tabla Stock
                try:
                    crear_tablas(cursor)
                except:
                    pass
                else:
                    insertar_tuplas_tabla_stock(cursor)
                    borrar_tabla('Stock',cursor)
            case 2:
                # Dar de alta un pedido
                alta_pedido(cursor)
            case 3:
                # Mostrar el contenido de las tablas
                pass
    
    # Cerramos conexión con la base de datos
    print("Cerrando conexión...")
    conexion.close()
    
###############################################################################

if __name__ == "__main__":
    main()