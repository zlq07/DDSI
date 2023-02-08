import oracledb

def crear_tablas(conexion: oracledb.Connection):
    """
        Crea las tablas necesarias en la base de datos.
    """
    with conexion.cursor() as cursor:
        # TABLA Mantenimiento:
        try:
            query = """CREATE TABLE MANTENIMIENTO(
                        ID_MANTENIMIENTO VARCHAR2(8),
                        ID_TRABAJADOR VARCHAR2(8),
                        ID_CONTENEDOR VARCHAR2(8),
                        TIPO_MANTENIMIENTO INT,
                        PRIMARY KEY (ID_MANTENIMIENTO)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Mantenimiento. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Mantenimiento.')
    with conexion.cursor() as cursor:
        # TABLA Historial-Mantenimiento:
        try:
            query = """CREATE TABLE HISTORIAL_MANTENIMIENTO(
                        ID_MANTENIMIENTO VARCHAR2(8),
                        ID_TRABAJADOR VARCHAR2(8),
                        ID_CONTENEDOR VARCHAR2(8),
                        TIPO_MANTENIMIENTO INT,
                        FECHA DATE
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Historial_mantenimiento. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Historial_mantenimiento.')
        # TABLA Ruta:
        try:
            query = """CREATE TABLE Ruta
                    (
                        id_ruta CHAR(6) CONSTRAINT id_ruta_no_nulo NOT NULL
                            CONSTRAINT id_ruta_clave_primaria PRIMARY KEY
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Ruta. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Ruta.')
        # TABLA Grupo_contenedores:
        try:
            query = """CREATE TABLE Grupo_contenedores
                    (
                        id_gr_cont CHAR(6) CONSTRAINT id_gr_cont_no_nulo NOT NULL
                            CONSTRAINT id_gr_cont_clave_primaria PRIMARY KEY,
                        ubic_gr_cont VARCHAR2(80) CONSTRAINT ubic_gr_cont_no_nulo NOT NULL,
                        lista_etiq VARCHAR2(11) CONSTRAINT lista_etiq_no_nulo NOT NULL
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Grupo_contenedores. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Grupo_contenedores.')
        # TABLA Usuario:
        try:
            query = """CREATE TABLE Usuario
                    (
                        id_usuario CHAR(6) CONSTRAINT id_usuario_no_nulo NOT NULL
                            CONSTRAINT id_usuario_clave_primaria PRIMARY KEY,
                        ubic_usuario VARCHAR2(80) CONSTRAINT ubic_usuario_no_nulo NOT NULL
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Usuario. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Usuario.')
        # TABLA Trayecto_Dirige:
        try:
            query = """CREATE TABLE Trayecto_Dirige
                    (
                        id_trayecto CHAR(6) CONSTRAINT id_trayecto_no_nulo NOT NULL
                            CONSTRAINT id_trayecto_clave_primaria PRIMARY KEY,
                        id_gr_cont CONSTRAINT id_gr_cont_cla_ext_Gru_cont
                            REFERENCES Grupo_contenedores(id_gr_cont)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Trayecto_Dirige. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Trayecto_Dirige.')
        # TABLA Guarda_fav:
        try:
            query = """CREATE TABLE Guarda_fav
                    (
                        id_usuario CONSTRAINT id_usuario_clave_ext_Usr_Gf
                            REFERENCES Usuario(id_usuario),
                        id_trayecto CONSTRAINT id_tray_clave_ext_Tray_Dir_Gf
                            REFERENCES Trayecto_Dirige(id_trayecto),
                        CONSTRAINT clave_primaria_Guarda_fav PRIMARY KEY(id_usuario, id_trayecto)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Guarda_fav. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Guarda_fav.')
        # TABLA Usa:
        try:
            query = """CREATE TABLE Usa
                    (
                        id_usuario CONSTRAINT id_usuario_clave_ext_Usa
                            REFERENCES Usuario(id_usuario),
                        id_trayecto CONSTRAINT id_trayecto_clave_ext_Usa
                            REFERENCES Trayecto_Dirige(id_trayecto),
                        CONSTRAINT clave_primaria_Usa PRIMARY KEY(id_usuario, id_trayecto)
                    )
                    """
            cursor.execute(query)
            
        except Exception as e:
            print(f'No se ha podido crear la tabla Usa. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Usa.')

        # TABLA Contenedor:
        try:
            query = """CREATE TABLE Contiene
                    (
                        id_gr_cont CONSTRAINT id_gr_cont_cla_ext_Gr_Cont
                            REFERENCES Grupo_contenedores(id_gr_cont),
                        id_ruta CONSTRAINT id_ruta_cla_ext_Ruta REFERENCES Ruta(id_ruta),
                        CONSTRAINT clave_primaria_Contiene PRIMARY KEY (id_gr_cont)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Contiene. {e}')
        except:
            print('ERROR EN CONTIENE')
        else:
            print(f'Se ha creado correctamente la tabla Contiene.')

        '''
        Tablas de subsistema 4
        '''
        # tabla camion
        try:
            query = """CREATE TABLE Camion(
                        ID_CAMION NUMBER(6) NOT NULL,
                        N_BASTIDOR VARCHAR2(17),
                        MATRICULA VARCHAR2(8),
                        FECHA_ULTIMA_REVISION DATE,
                        KILOMETRAJE NUMBER(10),
                        MMA NUMBER(10),
                        FECHA_MATRICULACION DATE,
                        PRIMARY KEY (ID_CAMION)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Camion. {e}')
        else: 
            print(f'Se ha podido crear la tabla Camion.')
        
        # TABLA Recorre:
        try:
            query = """CREATE TABLE Recorre
                    (
                        id_ruta CONSTRAINT id_ruta_cla_ext_Recorre
                            REFERENCES Ruta(id_ruta),
                        id_camion CONSTRAINT id_camion_cla_ext_Recorre
                            REFERENCES Camion(id_camion),
                        CONSTRAINT clave_primaria_Recorre PRIMARY KEY (id_ruta, id_camion)
                    )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Recorre. {e}')
        else:
            print(f'Se ha creado correctamente la tabla Recorre.')

        # tabla envio
        try:
            query = """CREATE TABLE Envio(
                            ID_ENVIO NUMBER(10),
                            TIPO_RESIDUO INT CONSTRAINT tipo_re_no_nulo NOT NULL,
                            PRIMARY KEY (ID_ENVIO)
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Envio. {e}')
        else: 
            print(f'Se ha podido crear la tabla Envio.')

        # tabla Gestor
        try:
            query = """CREATE TABLE Gestor(
                            ID_GESTOR NUMBER(10),
                            PRIMARY KEY (ID_GESTOR)
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Gestor. {e}')
        else: 
            print(f'Se ha podido crear la tabla Gestor.')


        # tabla Asigna
        try:
            query = """CREATE TABLE Asigna(
                            ID_GESTOR CONSTRAINT ID_GESTOR_CLAVE_EXT_GESTOR REFERENCES Gestor(ID_GESTOR),
                            ID_ENVIO CONSTRAINT ID_ENVIO_CLAVE_EXT_ENVIO REFERENCES Envio(ID_ENVIO),
                            ID_CAMION CONSTRAINT ID_CAMION_CLAVE_EXT_CAMION REFERENCES Camion(ID_CAMION),
                            CONSTRAINT clave_primaria_Asigna PRIMARY KEY (ID_GESTOR,ID_ENVIO)
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Asigna. {e}')
        else: 
            print(f'Se ha podido crear la tabla Asigna.')


        # tabla planta reciclaje
        try:
            query = """CREATE TABLE Planta_reciclaje(
                            ID_SERVICIO NUMBER(10),
                            TIPO_DE_SERVICIO VARCHAR(30),
                            CONSTRAINT clave_primaria_Pl_rec PRIMARY KEY(ID_SERVICIO)
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la planta. {e}')
        else: 
            print(f'Se ha podido crear la tabla Planta reciclaje.')


        # tabla peso_hora_supone
        try:
            query = """CREATE TABLE Peso_hora_supone(
                            ID_SERVICIO CONSTRAINT clave_primaria_ser REFERENCES Planta_reciclaje(ID_SERVICIO),
                            ID_CAMION CONSTRAINT ID_CAMION_CLAVE_EXT_CAMI REFERENCES Camion(ID_CAMION),
                            PESO_SALIDA NUMBER(10),
                            PESO_ENTRADA NUMBER(10),
                            HORA_SALIDA DATE,
                            HORA_ENTRADA DATE,
                            CONSTRAINT clav_pri_P_h_supone PRIMARY KEY (ID_SERVICIO,ID_CAMION)
                        )
                    """
            cursor.execute(query)
        except Exception as e:
            print(f'No se ha podido crear la tabla Peso_hora_supone. {e}')
        else: 
            print(f'Se ha podido crear la tabla Peso_hora_supone.')

        cursor.execute("COMMIT")
        print('\n')
