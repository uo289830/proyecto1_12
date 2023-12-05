from util.database import DataBase
import sqlite3
from datetime import datetime, timedelta
from util.checkdate import DateChecker  # Asegúrate de importar la clase DateChecker

class EntidadModel:
    
    def __init__(self):
        self.db = DataBase("deporte.db")
    def comprobarNomEnt(self,nombre):
        query="SELECT COUNT(*) from ActividadEntidades where nombre_entidad=?"
        s=self.db.executeQuery(query,(nombre,))
        s=s[0]['COUNT(*)']
        print(s)
        if s!=0:
            return False
        else:
            return True
        
    def comprobarNomActividad(self,nombre):
        query="SELECT COUNT(*) from ActividadEntidades where nombre_activ_entidad=?"
        s=self.db.executeQuery(query,(nombre,))
        s=s[0]['COUNT(*)']
        print(s)
        if s!=0:
            return False
        else:
            return True
    
    def comprobrarhora(sef,hora):
        horas=int(hora[0:2])
        mins=int(hora[3:])
        if horas>23 or horas<0:
            return False
        elif mins>59 or mins<0:
            return False
        else:
            return True       
        
    
      # Inserción de los datos de una actividad (historia de usuario1 - Adriana)
    def insertActividadEntidad(self,nombre_entidad, nombre_actividad, descripcion, fecha, duracion,hora_inicio, localizacion,plazas, coste,info_ad):
        while True:
            if not DateChecker.checkdateEntidad(fecha):
                print("La fecha no cumple con el formato esperado (aaaa-mm-dd).")
                fecha = input("Por favor, ingrese la fecha nuevamente (aaaa-mm-dd): ")
            else:
                break  # La fecha es válida, salimos del bucle
        query = """
                INSERT INTO ActividadEntidades(nombre_entidad, nombre_activ_entidad ,descripcion ,fecha ,duracion_dias,hora_inicio,lugar,plazas,coste_UsFree,info_adicional)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                """
        self.db.executeUpdateQuery(query,nombre_entidad, nombre_actividad, descripcion, fecha, duracion,hora_inicio, localizacion,plazas, coste,info_ad)


    def obtener_inscripciones(self, id_actividad):
        query = """
            SELECT ae.nombre_activ_entidad AS nombre_actividad, A.correo_electronico, A.tipo_atleta
            FROM Inscripciones i
            INNER JOIN ActividadEntidades ae ON i.idactividadentidad = ae.idactividadentidad
            INNER JOIN Atletas A ON i.correo_electronico = A.correo_electronico
            WHERE ae.idactividadentidad = ?
        """

        return self.db.executeQuery(query, (id_actividad,))
    
    def obtener_actividades_entidad(self, nombre_entidad):
        query = """
            SELECT idactividadentidad, nombre_activ_entidad
            FROM ActividadEntidades
            WHERE nombre_entidad = ?
        """
        return self.db.executeQuery(query, (nombre_entidad,))
