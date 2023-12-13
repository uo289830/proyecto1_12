from util.database import DataBase
import sqlite3
from datetime import datetime, timedelta


class GestorModel:
    
    def __init__(self):
        self.db = DataBase("deporte.db")
        
    
    def obtenerActividadesUltimoMes(self, correo_electronico):
        fecha_hace_un_mes = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        print(fecha_hace_un_mes)
        query = "SELECT COUNT(*) FROM Actividades WHERE correo_electronico = ? AND fecha <= ?"
        actividades_ultimo_mes = self.db.executeQuery(query, (correo_electronico, fecha_hace_un_mes))
        return actividades_ultimo_mes[0]['COUNT(*)'] if actividades_ultimo_mes else 0

    def obtenerTodasLasActividades(self, correo_electronico):
        query = "SELECT COUNT(*) FROM Actividades WHERE correo_electronico = ?"
        actividades_totales = self.db.executeQuery(query, (correo_electronico,))
        return actividades_totales[0]['COUNT(*)'] if actividades_totales else 0

    def calcularEstadoForma(self, correoElectronico):
        
        actividades_ultimo_mes = self.obtenerActividadesUltimoMes(correoElectronico)
        actividades_totales = self.obtenerTodasLasActividades(correoElectronico)

        estado_de_forma = actividades_ultimo_mes / actividades_totales if actividades_totales > 0 else 0.0

        return [actividades_ultimo_mes,actividades_totales,estado_de_forma]

    def obtenerDeportistasMasActivos(self, tipo_actividad):
        query = """
            SELECT A.correo_electronico AS correo_atleta, A.nombre AS nombre_atleta, A.fecha_alta,
            COUNT(Ac.idactividad) AS total_actividades FROM Atletas AS A
            INNER JOIN Actividades AS Ac ON A.correo_electronico = Ac.correo_electronico 
            WHERE Ac.nombre_actividad = ? GROUP BY A.correo_electronico, A.nombre, A.fecha_alta ORDER BY
            total_actividades DESC
        """
        return self.db.executeQuery(query, (tipo_actividad,))
    
    def obtener_num_deportistas_inscritos(self):
        query = """
            SELECT ae.nombre_entidad, ae.nombre_activ_entidad, COUNT(i.idinscripcion) AS num_inscritos, ae.fecha
            FROM ActividadEntidades ae
            LEFT JOIN Inscripciones i ON ae.idactividadentidad = i.idactividadentidad
            GROUP BY ae.nombre_entidad, ae.nombre_activ_entidad, ae.fecha

        """
        return self.db.executeQuery(query)