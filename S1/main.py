# encoding: utf-8
###############################################################################
import oracledb
from getpass import getpass
###############################################################################

# Imprime un menu con las opciones
def menu():
    """
        Imprime el menú principal por pantalla
    """
    print('Opciones:')
    print('\t1. Borrado y nueva creación de las tablas e inserción de 10 tuplas predefinidas en el código en la tabla Stock')
    print('\t2. Dar de alta un pedido')
    print('\t3. Mostrar contenido de las tablas')
    print('\t4. Salir del programa y cerrar conexión')

# Le dice al usuario que escoja una opción de las existentes
def escoger_opcion(min: int, max: int) -> int:
    """
        Solicitar al usuario un número entero en el intervalo `[min,max]`
        hasta que se cumpla dicha condición
    """
    opc = 0
    while (opc < min or opc > max):
        opc = int(input("Elija una opción: "))
    return opc

def crear_tablas(cursor: oracledb.cursor.Cursor):
    """
        Define y crea las tablas `Stock`, `Pedido` y `DetallePedido` en la
        base de datos
    """
    try:
        filepath: str = '../crear_tablas.sql'
        cursor.execute('START {}'.format(filepath))
    except Exception as e:
        print('No se pueden crear las tablas \n {}'.format(e))
    else:
        print('Se han creado las tablas correctamente')

def insertar_tuplas_tabla_stock(cursor: oracledb.cursor.Cursor):
    """
        Inserta 10 tuplas predefinidas en el fichero `insercion_tuplasPredefinidas_Stock.sql`
        en la tabla `Stock`
    """
    try:
        filepath: str = '../insercion_tuplasPredefinidas_Stock.sql'
        cursor.execute('START {}'.format(filepath))
    except Exception as e:
        print('No se pueden insertar las tuplas en Stock: \n {}'.format(e))
    else:
        print('Se han insertado las tuplas correctamente')

def borrar_tabla(cursor, tabla: str):
    """
        Borra la tabla de nombre `tabla` de la base de datos
    """
    try:
        cursor.execute('DROP TABLE {tabla};'.format(tabla))
    except Exception as e:
        print('No se han podido borrar las tabla {} \n {}'.format(tabla, e))
    else:
        print('Tabla {} borrada correctamente'.format(tabla))

def mostrar_bd(cursor: oracledb.cursor.Cursor):
    """
        Muestra las tablas Stock, Pedido y DetallePedido
        en la pantalla
    """
    def mostrar_tabla(tabla: str):
        print(f'\t---Tabla {tabla}---\t')
        try:
            for row in cursor.execute(f'SELECT * FROM {tabla}'):
                print(row)
        except Exception as e:
            print(f'Hubo un error al intentar mostrar la tabla {tabla}: \n {e}')
        
        # Tabla Stock
        mostrar_tabla('Stock')
        # Tabla Pedido
        mostrar_tabla('Pedido')
        # Tabla DetallePedido
        mostrar_tabla('DetallePedido')


def alta_pedido(cursor: oracledb.cursor.Cursor):

    codigo_producto: str = None
    cantidad_bd: int = 0
    cantidad_cliente: int = 0

    def menu_pedido():
        """
            Imprime el menú secundario correspondiente a la funcionalidad
            de dar de alta un pedido
        """
        print('Opciones:')
        print('1. Añadir los detalles del pedido')
        print('2. Eliminar todos los detalles del pedido')
        print('3. Cancelar')
        print('4. Terminar')

    def aniadir_detalle():
        """
            Le pide al usuario que inserte detalles sobre el pedido que va a realizar:
            - El código del producto
                - Debe existir en la base de datos y debe haber existencias de ese producto
            - La cantidad que desea
                - Debe ser un número del intervalo `(0, cantidad_bd]`
            Una vez terminado, se inserta en la base de datos una nueva tupla en `DetallePedido`
            con los datos solicitados
        """
        # Obtenemos la cantidad del producto correspondiente de la tabla Stock
        while (cantidad_bd <= 0):
            try:
                codigo_producto: str = input("Inserte código de producto: ")
                query = f'SELECT Cantidad FROM Stock WHERE Cproducto={codigo_producto}'
                cantidad_bd = cursor.execute(query).fetchone()[0]
            except Exception as e:
                print(f'Ha ocurrido un error con la base de datos: \n {e}')
                return
            else:
                if (cantidad_bd <= 0):
                    print('No hay existencias del producto solicitado')
                else:
                    print(f'Existen {cantidad_bd} unidades del producto solicitado')

        # Ahora le pedimos al usuario la cantidad de productos que desea pedir
        # No es valido mientras la cantidad supera el maximo permitido o es menor o igual a cero
        while (cantidad_cliente <= 0 or cantidad_cliente > cantidad_bd):
            cantidad_cliente = int(input('Cantidad a pedir: '))
            if (cantidad_cliente > cantidad_bd):
                print('La cantidad debe ser menor o igual a las existencias disponibles')
        
        # TODO
        # Una vez tenemos bien todos los datos solicitados, creamos una nueva tupla en
        # la tabla DetallesPedido (Cpedido, Cproducto, cantidad)
        # Tambien deberiamos hacer lo de las transferencias

        # Finalmente:
        # print('Se ha detallado el pedido correctamente')
        # print('Codigo pedido')
        # print('Codigo producto')
        # print('Cantidad')
        # ------------------------------------------------

    # TODO
    def eliminar_detalle():
        """
            Eliminar todos los detalles SOLO en detalle-pedido
            #? Las variables del codigo de producto y de la cantidad deberian estar definidas en alta pedido?
        """
        try:
            pass
        except:
            print('Error al intentar borrar los detalles del pedido')
        else:
            print('Detalles del pedido borrados correctamente')
    
    def cancelar():
        """
            borrar tupla de pedido y salir
        """
        try:
            pass
        except:
            print('Error al cancelar el pedido')
        else:
            print('Pedido cancelado correctamente')

    def terminar():
        print('Saliendo del menú de altas...')

    # Crear pedido
    menu_pedido()
    opc = None
    # Mientras no se cancele o se termine el pedido
    while (opc not in [3, 4]):
        opc = escoger_opcion(1,4)
        match opc:
            case 1:
                aniadir_detalle()
                mostrar_bd()
            case 2:
                eliminar_detalle()
                mostrar_bd()
            case 3:
                cancelar()
                mostrar_bd()
            case 4:
                terminar()
        if (opc != 4): 
            # Mostrar todas las tablas
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
                mostrar_bd()
    
    # Cerramos conexión con la base de datos
    print("Cerrando conexión...")
    conexion.close()
    
###############################################################################

if __name__ == "__main__":
    main()