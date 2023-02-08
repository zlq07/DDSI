
import oracledb

def crear_disparadores (conexion: oracledb.Connection):
    """
        Crea los disparadores del SI.
    """
    with conexion.cursor() as cursor:

        # Disparador 1 del subsistema de Localización de Contenedores:
        """
            Disparador 1 del subsistema de Localización de Contenedores.
            Sirve para mantener la consistencia entre los trayectos usados por los
            usuarios y los almacenados como favoritos. Cuando se realiza un borrado
            en la tabla Usa, en caso de estar esa misma información en los favoritos,
            será también eliminada de esa tabla.
        """
        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER Tr_controlar_tray_fav
                                AFTER DELETE ON Usa FOR EACH ROW
                            DECLARE
                                id_usr Usa.id_usuario%TYPE := :OLD.id_usuario;
                                id_tray Usa.id_trayecto%TYPE := :OLD.id_trayecto;
                            BEGIN
                                DELETE FROM Guarda_fav WHERE (id_usuario = id_usr) AND (id_trayecto = id_tray);
                            END Tr_controlar_tray_fav;
                        """)
        except Exception as e:
            print(f'No se ha podido crear el disparador Tr_controlar_tray_fav. {e}')
        else:
            print(f'Se ha creado correctamente el disparador Tr_controlar_tray_fav.')

        # Disparador 2 del subsistema de Localización de Contenedores:
        """
            Disparador 2 del subsistema de Localización de Contenedores.
            Sirve para mantener la consistencia entre los trayectos favoritos de los
            usuarios y los almacenados como usados por ellos. Cuando se realiza una inserción
            en la tabla Guarda_fav, en caso de no estar esa misma información en los trayectos
            usados por el usuario, será también almacenada en esta última tabla (Usa).
        """
        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER Tr_controlar_tray_usa
                                AFTER INSERT ON Guarda_fav FOR EACH ROW
                            DECLARE
                                id_usr Guarda_fav.id_usuario%TYPE := :NEW.id_usuario;
                                id_tray Guarda_fav.id_trayecto%TYPE := :NEW.id_trayecto;
                                num_tuplas NUMBER;
                            BEGIN
                                SELECT COUNT(*) INTO num_tuplas FROM Usa WHERE (id_usuario = id_usr) AND (id_trayecto = id_tray);
                                IF (num_tuplas = 0) THEN
                                    INSERT INTO Usa VALUES (id_usr, id_tray);
                                END IF;
                            END Tr_controlar_tray_usa;
                        """)
        except Exception as e:
            print(f'No se ha podido crear el disparador Tr_controlar_tray_usa. {e}')
        else:
            print(f'Se ha creado correctamente el disparador Tr_controlar_tray_usa.')
            # Disparador 1 del subsistema de Gestión y Mantenimiento de Camiones y Contenedores:
        """
            Disparador 1 del subsistema de Gestión y Mantenimiento de Camiones y Contenedores.
        """
        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER Tr_historial_mantenimiento
                                AFTER DELETE ON MANTENIMIENTO
                            FOR EACH ROW
                            BEGIN
                                INSERT INTO HISTORIAL_MANTENIMIENTO 
                                VALUES (:OLD.ID_MANTENIMIENTO, :OLD.ID_TRABAJADOR, :OLD.ID_CONTENEDOR, :OLD.TIPO_MANTENIMIENTO, SYSDATE);
                            END Tr_controlar_mantenimiento;
                        """)
        except Exception as e:
            print(f'No se ha podido crear el disparador Tr_controlar_tray_usa. {e}')
        else:
            print(f'Se ha creado correctamente el disparador Tr_controlar_mantenimiento.')

    # Disparador 1 del subsistema de Gestión de la planta
        """
            Disparador 1 del subsistema de Gestión Gestión de la planta
            No puede modificar tipo de residuo de un envio si ya esta asociado asinado al camion 
        """
        try:
            cursor.execute("""create or replace TRIGGER modificar_tipo_residuo
                                BEFORE UPDATE ON Envio 
                                FOR EACH ROW
                                DECLARE
                                existe INT;
                                error_asignacion EXCEPTION;
                                BEGIN
                                    SELECT COUNT(*) INTO existe FROM Asigna Where ID_ENVIO =: NEW.ID_ENVIO;
                                    dbms_output.put_line(existe);
                                    IF(existe>0) THEN
                                        RAISE error_asignacion;
                                    END IF;
                                EXCEPTION 
                                    WHEN error_asignacion THEN
                                    dbms_output.put_line('ERROR EXISTE, ya esta asignado a un camion');
                                    raise_application_error(-20001,'Ya esta asignado a un camion');
                                END;   
                        """)
        except Exception as e:
            print(f'No se ha podido crear el disparador modificar_tipo_residuo. {e}')
        else:
            print(f'Se ha creado correctamente el disparador modificar_tipo_residuo.')

        # SUBSISTEMA 2
        """
            Estos tres disparadores se encargan de borrar las tuplas de las tablas que contienen
            referencias externas a las tuplas de las tablas Ruta, Grupo_contenedores y Camion para que
            no de errores a la hora de borrar directamente de la base de datos una ruta, un grupo de
            contenedores o un camion, manteniendo asi la coherencia de los datos
        """
        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER borrar_refs_ruta
                            BEFORE DELETE ON Ruta
                            FOR EACH ROW
                            BEGIN
                                DELETE FROM Contiene WHERE id_ruta=:old.id_ruta;
                                DELETE FROM Recorre WHERE id_ruta=:old.id_ruta;
                            END;
            """)
        except Exception as e:
            print(
                f'No se ha podido crear el disparador borrar_referencias_ruta. {e}')
        else:
            print(f'Se ha creado correctamente el disparador borrar_referencias_ruta.')

        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER borrar_refs_grupo_contenedores
                            BEFORE DELETE ON Grupo_contenedores
                            FOR EACH ROW
                            BEGIN
                                DELETE FROM Contiene WHERE id_gr_cont=:old.id_gr_cont;
                            END;
            """)
        except Exception as e:
            print(
                f'No se ha podido crear el disparador borrar_referencias_grupo_contenedores. {e}')
        else:
            print(
                f'Se ha creado correctamente el disparador borrar_referencias_grupo_contenedores.')

        try:
            cursor.execute("""CREATE OR REPLACE TRIGGER borrar_refs_camiones
                            BEFORE DELETE ON Camion
                            FOR EACH ROW
                            BEGIN
                                DELETE FROM Recorre WHERE id_camion=:old.id_camion;
                            END;
            """)
        except Exception as e:
            print(
                f'No se ha podido crear el disparador borrar_refs_camiones. {e}')
        else:
            print(f'Se ha creado correctamente el disparador borrar_refs_camiones.')
