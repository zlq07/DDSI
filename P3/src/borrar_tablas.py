
import oracledb

def borrar_tablas(conexion: oracledb.Connection):
    """
        Borra las tablas de la BD.
    """
    print('\nBorrando tablas...\n') 
    def borrar_tabla(tabla: str):
        """
            Borra la tabla con nombre `tabla` de la base de datos
        """
        with conexion.cursor() as cursor:
            try:
                existe: bool = cursor.execute(
                    f'SELECT TABLE_NAME FROM USER_TABLES WHERE TABLE_NAME=\'{tabla.upper()}\'').fetchone() != None
                if existe:
                    cursor.execute(f'DROP TABLE {tabla}')
                    print(f'Tabla {tabla} borrada correctamente.')
                else:
                    print(f'La tabla {tabla} no existe, no se puede borrar.')
                    return
            except Exception as e:
                print(f'No se ha podido borrar la tabla {tabla}. \n {e}')

    borrar_tabla('Mantenimiento')
    borrar_tabla('Historial_Mantenimiento')
    borrar_tabla('Usa')
    borrar_tabla('Guarda_fav')
    borrar_tabla('Trayecto_Dirige')
    borrar_tabla('Usuario')
    borrar_tabla('Contiene')
    borrar_tabla('Recorre')
    borrar_tabla('Grupo_contenedores')
    borrar_tabla('Ruta')
    borrar_tabla('Asigna')
    borrar_tabla('Envio')
    borrar_tabla('Gestor')
    borrar_tabla('Peso_hora_supone')
    borrar_tabla('Planta_reciclaje')
    borrar_tabla('Camion')
    conexion.cursor().execute("COMMIT")
    print('\n')