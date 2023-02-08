
import oracledb

def insertar_tuplas_tablas_sub1(conexion: oracledb.Connection):
    ########################################################################################
    def insertar_tuplas_tabla_Ruta():
        """
            Inserta 10 tuplas predefinidas en la tabla 'Ruta'.
        """
        with conexion.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO Ruta VALUES ('590342')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('290145')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('824517')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('678810')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('391127')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('378912')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('389012')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('289012')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('190378')")
                cursor.execute(f"INSERT INTO Ruta VALUES ('190569')")
            except Exception as e:
                print(f'No se pueden insertar las tuplas en Ruta: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Ruta.')
                cursor.execute("COMMIT")

    def insertar_tuplas_tabla_Grupo_contenedores():
        """
            Inserta 10 tuplas predefinidas en la tabla 'Grupo_contenedores'.
        """
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('123456','-34.622041, -58.37066','OCVPER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('467248','-19.041949, -65.264373','OCVPER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('014782','-33.444760, -70.654342','OCVER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('639016','4.658653, -74.094160','OCVER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('320422','9.932839, -84.071680','OCV')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('211075','-0.236329, -78.516035','OVPER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('007492','40.413888, -3.691844','OCPER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('792556','14.641828, -90.513080','OCVPER')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('915936','14.094285, -87.200521','OVR')")
                cursor.execute(
                    f"INSERT INTO Grupo_contenedores VALUES ('674367','19.427061, -99.167601','PE')")

            except Exception as e:
                print(
                    f'No se pueden insertar las tuplas en Grupo_contenedores: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Grupo_contenedores.')
                cursor.execute("COMMIT")

    def insertar_tuplas_tabla_Contiene():
        with conexion.cursor() as cursor:
            try:
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('123456', '590342')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('467248', '590342')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('014782', '590342')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('639016', '824517')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('320422', '824517')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('211075', '391127')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('007492', '391127')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('792556', '190569')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('915936', '190378')")
                cursor.execute(f"INSERT INTO Contiene (id_gr_cont, id_ruta) VALUES ('674367', '190378')")
            except Exception as e:
                print(f'No se han podido insertar las tuplas en la tabla Contiene: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Contiene.')
                cursor.execute("COMMIT")


    def insertar_tuplas_tabla_Camiones():
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO Camion (ID_CAMION,N_BASTIDOR) VALUES ('123401','1HGBH41JXMN109186')")
                cursor.execute(
                    f"INSERT INTO Camion (ID_CAMION,N_BASTIDOR) VALUES ('123502','1VBIPIUWEER110110')")
                cursor.execute(
                    f"INSERT INTO Camion (ID_CAMION,N_BASTIDOR) VALUES ('123603','1JBJLMSNDZN128302')")
            except Exception as e:
                print(f'No se pueden insertar las tuplas en Camion: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Camion.')
                cursor.execute('COMMIT')
        pass


    def insertar_tuplas_tabla_Recorre():
        with conexion.cursor() as cursor:
            cursor.execute('SAVEPOINT tuplas_tabla_recorre')
            try:
                cursor.execute(
                    f"INSERT INTO Recorre VALUES ('590342', '123401')")
                cursor.execute(
                    f"INSERT INTO Recorre VALUES ('678810', '123502')")
                cursor.execute(
                    f"INSERT INTO Recorre VALUES ('824517', '123603')")
            except Exception as e:
                print(f'No se pueden insertar las tuplas en Recorre: {e}')
                cursor.execute('ROLLBACK TO tuplas_tabla_recorre')
            else:
                print('Se han insertado las tuplas correctamente en Recorre.')
                cursor.execute('COMMIT')
        pass
    ########################################################################################
    insertar_tuplas_tabla_Ruta()
    insertar_tuplas_tabla_Grupo_contenedores()
    insertar_tuplas_tabla_Contiene()
    insertar_tuplas_tabla_Camiones()
    insertar_tuplas_tabla_Recorre()
    

def insertar_tuplas_tablas_sub3(conexion: oracledb.Connection):
############################################################################################
    def insertar_tuplas_tabla_Usuario ():
        """
            Inserta 10 tuplas predefinidas en la tabla 'Usuario'.
        """
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('950256','-35.633041, -56.37023')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('078324','-17.092949, -66.264483')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('178943','-31.444650, -71.653342')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('095834','5.658753, -73.095160')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('092674','10.956839, -80.091680')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('093672','-0.236256, -77.516535')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('018943','41.413999, -3.691855')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('104839','13.641867, -91.713080')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('578934','16.094146, -86.201521')")
                cursor.execute(
                    f"INSERT INTO Usuario VALUES ('105923','18.429161, -99.167603')")

            except Exception as e:
                print(f'No se pueden insertar las tuplas en Usuario: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Usuario.')
                cursor.execute("COMMIT")

    def insertar_tuplas_tabla_Trayecto_Dirige ():
        """
            Inserta 10 tuplas predefinidas en la tabla 'Trayecto_Dirige'.
        """
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('593491','123456')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('053349','467248')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('126934','014782')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('001234','639016')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('098765','320422')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('873467','211075')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('189426','007492')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('105693','792556')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('489345','915936')")
                cursor.execute(
                    f"INSERT INTO Trayecto_Dirige VALUES ('073999','674367')")
            except Exception as e:
                print(f'No se pueden insertar las tuplas en Trayecto_Dirige: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Trayecto_Dirige.')
                cursor.execute("COMMIT")

    def insertar_tuplas_tabla_Usa ():
        """
            Inserta 10 tuplas predefinidas en la tabla 'Usa'.
        """
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('950256','593491')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('078324','053349')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('178943','126934')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('095834','001234')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('092674','098765')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('093672','873467')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('018943','189426')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('104839','105693')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('578934','489345')")
                cursor.execute(
                    f"INSERT INTO Usa VALUES ('105923','073999')")
            except Exception as e:
                print(f'No se pueden insertar las tuplas en Usa: {e}')
            else:
                print('Se han insertado las tuplas correctamente en Usa.')
                cursor.execute("COMMIT")

    insertar_tuplas_tabla_Usuario ()
    insertar_tuplas_tabla_Trayecto_Dirige ()
    insertar_tuplas_tabla_Usa ()


def insertar_tuplas_tablas_sub4(conexion: oracledb.Connection):
    with conexion.cursor() as cursor:
        try:
            cursor.execute(
                f"INSERT INTO Camion (ID_CAMION,N_BASTIDOR) VALUES ('1234','1HGBH41JXMN109186')")
        except Exception as e:
            print(f'No se pueden insertar las tuplas en Camion:\n {e}')
        else:
            print('Se han insertado las tuplas correctamente en Camion.')
            cursor.execute("COMMIT")

        try:
            cursor.execute(
                f"INSERT INTO Envio VALUES ('1234','1')")
        except Exception as e:
            print(f'No se pueden insertar las tuplas en Envio: {e}')
        else:
            print('Se han insertado las tuplas correctamente del Envio.')
            cursor.execute("COMMIT")

        try:
            cursor.execute(
                f'INSERT INTO Gestor VALUES (1)')
            cursor.execute(
                f'INSERT INTO Gestor VALUES (2)')
        except Exception as e:
            print(f'No se pueden insertar las tuplas en Gestor: {e}')
        else:
            print('Se han insertado las tuplas correctamente en Gestor.')
            cursor.execute("COMMIT")
        
        try:
            cursor.execute(
                f"INSERT INTO Planta_reciclaje VALUES ('12','pesar')")
        except Exception as e:
            print(f'No se pueden insertar las tuplas en Planta_reciclaje: {e}')
        else:
            print('Se han insertado las tuplas correctamente del Planta_reciclaje.')
            cursor.execute("COMMIT")

    print('\n')