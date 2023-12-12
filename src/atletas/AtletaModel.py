from util.database import DataBase
import sqlite3
from datetime import datetime, timedelta
from actividades.ActividadModel import ActividadModel
from gestores.GestorModel import GestorModel
from util.checkdate import DateChecker
from dateutil.relativedelta import relativedelta 
import csv
from prettytable import PrettyTable
import sys

class AtletaModel:
    
    def __init__ (self):
        self.db = DataBase ("deporte.db")
        self.actividad_model=ActividadModel()

    def busca_actividades(self, correo_electronico, fecha_inicio, fecha_fin):
        if not DateChecker.checkdate(fecha_inicio) or not DateChecker.checkdate(fecha_fin):
            print("Error: Las fechas no tienen el formato válido (aaaa-mm-dd).")
        # Muestra los datos del atleta
        query1 = "SELECT * FROM Atletas WHERE correo_electronico = ?"
        atletas = self.db.executeQuery(query1, (correo_electronico,))
        for atleta in atletas:
            print(f"Correo: {atleta['correo_electronico']}, Nombre: {atleta['nombre']}, Apellidos: {atleta['apellidos']}")
        # Asegúrate de que las fechas sean cadenas en el formato "aaaa-mm-dd"
        fecha_inicio = str(fecha_inicio)
        fecha_fin = str(fecha_fin)
        correo_electronico = str(correo_electronico)
        fecha_actual = datetime.now()
        fecha_limite_free = fecha_actual - timedelta(days=365)
        fecha_limite_free=str(fecha_limite_free)
        # Recupera y muestra los detalles de las actividades en el rango de fechas.
        # Añade la condición para limitar la visualización al último año para usuarios Free
        query = "SELECT * FROM Actividades WHERE correo_electronico = ? AND fecha >= ? AND fecha <= ?"
        if self.actividad_model.esDeportistaFree(correo_electronico) and fecha_limite_free>fecha_inicio:
            valor=(correo_electronico, fecha_limite_free, fecha_fin)
            
        else:
            valor=(correo_electronico, fecha_inicio, fecha_fin)

        actividades = self.db.executeQuery(query, valor)
        return actividades


    def resumen(self, correo_electronico):
        atleta_query = "SELECT * FROM Atletas WHERE correo_electronico = ?"
        actividades_natacion_query = "SELECT COUNT(idactividad) AS sesiones, SUM(distancia) AS disttot FROM Actividades WHERE nombre_actividad = 'natacion' AND correo_electronico = ?"
        actividades_atletismo_query = "SELECT COUNT(idactividad) AS sesiones, SUM(distancia) AS disttot FROM Actividades WHERE nombre_actividad = 'atletismo' AND correo_electronico = ?"

        atleta = self.db.executeQuery(atleta_query, (correo_electronico,))

        if atleta:
            atleta = atleta[0]
            print(f"Correo: {atleta['correo_electronico']}, Nombre: {atleta['nombre']}, Apellidos: {atleta['apellidos']}")

            actividades_natacion = self.db.executeQuery(actividades_natacion_query, (correo_electronico,))[0]
            actividades_atletismo = self.db.executeQuery(actividades_atletismo_query, (correo_electronico,))[0]

            print(f"Natación: Sesiones: {actividades_natacion['sesiones']}, Distancia total: {actividades_natacion['disttot']} km")
            print(f"Atletismo: Sesiones: {actividades_atletismo['sesiones']}, Distancia total: {actividades_atletismo['disttot']} km")

            # Calcula y muestra el estado de forma
            gestor=GestorModel()
            estado_forma = gestor.calcularEstadoForma(correoElectronico=correo_electronico) # type: ignore
            print(f"Estado de forma: {estado_forma:.2f}")
        else:
            print("No se encontró un atleta con ese correo electrónico.")
    
    def getAtletasPremium(self):
        query = """select correo_electronico, tipo_atleta from Atletas where tipo_atleta='Premium'"""
        return self.db.executeQuery(query)

    #Obtiene el id de una actividad especificada por su nombre.
    def getIdactividad(self, nameactividad):
        query = """SELECT idactividad FROM Actividades
                WHERE Actividades.nombre_actividad = ?
                """

        res = self.db.executeQuery(query, (nameactividad,))

        if len(res) == 1:
            return res[0].get("idactividad")
        else:
            return None  
    
    
    def historia2(self,nameactividad,correo_electronico):
        query="""select A.correo_electronico as correo, A.nombre as nombre, A.apellidos as apellidos,
             Ac.fecha as fecha, Ac.duracion as duracion, Ac.distancia as distancia from Atletas as A
             inner join Actividades as Ac On A.correo_electronico=Ac.correo_electronico where Ac.nombre_actividad=? and A.correo_electronico=? order by fecha asc """
        return self.db.executeQuery(query,(nameactividad,correo_electronico))
    
    ##Calcular el consumo calórico
    def calcular_edad(self,fecha):
        fecha_nacimiento = datetime.strptime(str(fecha), "%Y-%m-%d")
        edad = relativedelta(datetime.now(), fecha_nacimiento)
        años=edad.years 
        return años
    
    #obtener el met de la actividad
    def obtenerMet (self,subtipo,correo,sexo):
        query="SELECT peso from Atletas where correo_electronico=?"
        peso=self.db.executeQuery(query,(correo,))
        peso=peso[0]['peso']
        peso=float(peso)
        query="SELECT Altura from Atletas where correo_electronico=?"
        altura=self.db.executeQuery(query,(correo,))
        altura=altura[0]['Altura']
        altura=float(altura)
        query="SELECT fecha_nacimiento from Atletas where correo_electronico=?"
        fecha_nacimiento=self.db.executeQuery(query,(correo,))
        fecha_nacimiento=fecha_nacimiento[0]['fecha_nacimiento']
        edad=self.calcular_edad(fecha_nacimiento)
        edad=float(edad)
        sexo=str(sexo)
        subtipo=str(subtipo)
        query="SELECT met from Subtipos where nombre_subtipo=?"
        met= self.db.executeQuery(query,(subtipo,))
        met=met[0]['met']
        if sexo=='hombre':
            MBR=10*peso+6.25*altura-(5*edad) + 5
        else:
            MBR=(10*peso)+(6.25*altura)-(5*edad) - 161
            
        consumo=(MBR/24/60)*met
        return consumo
        
        
    
    def calcularConsumo(self,correoelectronico,inicio,fin,sexo):
        #obtenemos las actividades en esa fecha
        actividades=AtletaModel.busca_actividades(self,correoelectronico,inicio,fin)
        listaconsumos=[]
        min=20
        max=0
        for actividad in actividades:
            subtipo= actividad['nombre_subtipo']
            print(subtipo)
            consumo= AtletaModel.obtenerMet(self,subtipo,correoelectronico,sexo) # type: ignore
            listaconsumos.append(consumo)
            if consumo<min:
                min=consumo
            if consumo>max:
                max=consumo
            print(f"Para la actividad {actividad['nombre_actividad']} el dia {actividad['fecha']} se obtuvo un consumo de {consumo}")
        consumototal= sum(listaconsumos)
        print(f"Consumo total: {consumototal}, Consumo minimo: {min}, Consumo maximo: {max}")
        return consumototal
        
             
    #h1s2 sara
    
    def obtenerActividadesDelMes(self, correo_electronico):
        fecha_actual = datetime.now()
        n = 1
        fecha_hace_un_mes = fecha_actual - relativedelta(months=n)
        
        query = """
            SELECT COUNT(*) AS total_actividades, fecha, SUM(duracion) as duracion_total, SUM(distancia) as distancia_total
            FROM Actividades
            WHERE correo_electronico = ? AND fecha BETWEEN ? AND ?
            GROUP BY fecha
        """
        resumen_mensual = self.db.executeQuery(query, (correo_electronico, fecha_hace_un_mes, fecha_actual))
        
        # Crear la tabla
        table = PrettyTable()
        table.field_names = ["Fecha", "Total Actividades", "Duración Total", "Distancia Total"]

        # Agregar filas a la tabla
        for item in resumen_mensual:
            table.add_row([item['fecha'], item['total_actividades'], item['duracion_total'], item['distancia_total']])
        
        return str(table)

    def obtenerActividadesDelAño(self, correo_electronico):
        fecha_actual = datetime.now()
        n = 12
        fecha_hace_un_año = fecha_actual - relativedelta(months=n)
        
        query = """
            SELECT strftime('%Y', fecha) as anio, COUNT(*) AS total_actividades, SUM(duracion) as duracion_total, SUM(distancia) as distancia_total
            FROM Actividades
            WHERE correo_electronico = ? AND fecha BETWEEN ? AND ?
            GROUP BY anio
        """
        resumen_anual = self.db.executeQuery(query, (correo_electronico, fecha_hace_un_año, fecha_actual))
        
        # Crear la tabla
        table = PrettyTable()
        table.field_names = ["Año", "Total Actividades", "Duración Total", "Distancia Total"]

        # Agregar filas a la tabla
        for item in resumen_anual:
            table.add_row([item['anio'], item['total_actividades'], item['duracion_total'], item['distancia_total']])
        
        return str(table)

    def obtenerActividadesPorTipoDelMes(self, correo_electronico):
        fecha_actual = datetime.now()
        n = 1
        fecha_hace_un_mes = fecha_actual - relativedelta(months=n)
        
        querytipos = """
            SELECT DISTINCT(nombre_subtipo) 
            FROM Subtipos
        """
        tipos = self.db.executeQuery(querytipos,)

        actividades_tipos_mes = {}
        
        for tipo in tipos:
            query = """
                SELECT nombre_subtipo, COUNT(*) AS total_actividades, SUM(duracion) as duracion_total, SUM(distancia) as distancia_total
                FROM Actividades
                WHERE correo_electronico = ? AND nombre_subtipo= ? AND fecha BETWEEN ? AND ?
            """

            actividades_por_tipo = self.db.executeQuery(query, (correo_electronico, tipo['nombre_subtipo'], fecha_hace_un_mes, fecha_actual))
            
            # Crear la tabla para cada tipo
            table = PrettyTable()
            table.field_names = ["Tipo", "Total Actividades", "Duración Total", "Distancia Total"]

            # Agregar filas a la tabla
            for item in actividades_por_tipo:
                table.add_row([item['nombre_subtipo'], item['total_actividades'], item['duracion_total'], item['distancia_total']])
            
            actividades_tipos_mes[tipo['nombre_subtipo']] = str(table)
        
        return actividades_tipos_mes

    def obtenerActividadesPorTipoDelAño(self, correo_electronico):
        fecha_actual = datetime.now()
        n = 12
        fecha_hace_un_año = fecha_actual - relativedelta(months=n)
        
        querytipos = """
            SELECT DISTINCT(nombre_subtipo) 
            FROM Subtipos
        """
        tipos = self.db.executeQuery(querytipos,)
        
        actividades_tipos_año = {}
        
        for tipo in tipos:
            query = """
                SELECT nombre_subtipo, COUNT(*) AS total_actividades, SUM(duracion) as duracion_total, SUM(distancia) as distancia_total
                FROM Actividades
                WHERE correo_electronico = ? AND nombre_subtipo= ? AND fecha BETWEEN ? AND ?
            """
            actividades_por_tipo = self.db.executeQuery(query, (correo_electronico, tipo['nombre_subtipo'], fecha_hace_un_año, fecha_actual))
            
            # Crear la tabla para cada tipo
            table = PrettyTable()
            table.field_names = ["Tipo", "Total Actividades", "Duración Total", "Distancia Total"]

            # Agregar filas a la tabla
            for item in actividades_por_tipo:
                table.add_row([item['nombre_subtipo'], item['total_actividades'], item['duracion_total'], item['distancia_total']])
            
            actividades_tipos_año[tipo['nombre_subtipo']] = str(table)
        
        return actividades_tipos_año


#h2s2 sara
    def importarActividadesDesdeCSV(self, ruta_archivo_csv):
        try:
            with open(ruta_archivo_csv, 'r') as archivo_csv:
                lector_csv = csv.DictReader(archivo_csv)
                for fila in lector_csv:
                    try:
                        # Llama a la función insertActividad con los datos de cada fila del CSV
                        self.actividad_model.insertActividad(
                            fila['nombre_actividad'],
                            fila['nombre_subtipo'],
                            fila['fecha'],
                            fila['duracion'],
                            fila['localizacion'],
                            fila['distancia'],
                            fila['FCmax'],
                            fila['FCmin'],
                            fila['correo_electronico']
                        )
                        print(f"Actividad importada: {fila}")
                    except Exception as e:
                        print(f"Error al insertar actividad. Fila: {fila}. Error: {e}")
            print("Importación de actividades exitosa.")
        except Exception as e:
            print(f"Error durante la importación de actividades: {e}")

        print("Importación completada.")


    def insertAtletaFree(self, Correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,Iban,Numero_tarjeta,fecha_caducidad,Cvv):
        while True:
            if not DateChecker.checkdate(fecha_nacimiento):
                print("La fecha no cumple con el formato esperado (aaaa-mm-dd).")
                fecha_nacimiento = input("Por favor, ingrese la fecha nuevamente (aaaa-mm-dd): ")
            else:
                break  # La fecha es válida, salimos del bucle
        query = """
                INSERT INTO Atletas(correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,IBAN,Numero_tarjeta,
                                     fecha_caducidad,CVV)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        self.db.executeUpdateQuery(query, Correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,Iban,Numero_tarjeta,fecha_caducidad,Cvv)

    def insertAtletaPremium(self, Correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,Iban,Numero_tarjeta,fecha_caducidad,Cvv):
        while True:
            if not DateChecker.checkdate(fecha_nacimiento):
                print("La fecha no cumple con el formato esperado (aaaa-mm-dd).")
                fecha_nacimiento = input("Por favor, ingrese la fecha nuevamente (aaaa-mm-dd): ")
            else:
                break  # La fecha es válida, salimos del bucle
        query = """
                INSERT INTO Atletas(correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,IBAN,Numero_tarjeta,
                                     fecha_caducidad,CVV)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        self.db.executeUpdateQuery(query, Correo_electronico,Nombre,Apellidos,fecha_alta,fecha_nacimiento,peso,Altura,tipo_atleta,Iban,Numero_tarjeta,fecha_caducidad,Cvv)


    def objetivos(self, correo_electronico, tipo_objetivo, valor_objetivo):
        query = """
        INSERT INTO Objetivos(correo_electronico, tipo_objetivo, valor_objetivo)
        VALUES (?, ?, ?)
        """
        self.db.executeQuery(query, (correo_electronico, tipo_objetivo, valor_objetivo))

    
    def getAtletas(self):
        query="""SELECT correo_electronico from Atletas"""
        return self.db.executeQuery(query)
    

    def getObjetivos(self, correo_electronico):
        query = """SELECT correo_electronico, tipo_objetivo, valor_objetivo from Objetivos where correo_electronico=?"""
        return self.db.executeQuery(query, (correo_electronico,))

    
    def getnumhoras(self, params):
        query = """SELECT sum(duracion) from Actividades WHERE (fecha BETWEEN ? AND ?) AND correo_electronico = ?"""
        result = self.db.executeQuery(query, params)
        return result[0]['sum(duracion)'] if result and result[0]['sum(duracion)'] is not None else 0

    def getnumactividades(self, params):
        query = """SELECT count(idactividad) from Actividades WHERE (fecha BETWEEN ? AND ?) AND correo_electronico = ?"""
        result = self.db.executeQuery(query, params)
        return result[0]['count(idactividad)'] if result and result[0]['count(idactividad)'] is not None else 0


    def obtenerActividadesExternas(self):
        query="SELECT nombre_entidad , nombre_activ_entidad ,descripcion ,fecha ,duracion_dias ,lugar ,plazas,coste_UsFree from ActividadEntidades"
        from prettytable import PrettyTable

    def obtenerActividadesExternas(self):
        query = "SELECT nombre_entidad, nombre_activ_entidad, descripcion, fecha, duracion_dias, lugar, plazas, coste_UsFree FROM ActividadEntidades"
        resultados = self.db.executeQuery(query)
        if resultados:
        # Obtener los nombres de las columnas
        
            columnas = resultados[0].keys()

        # Crear una tabla
            tabla = PrettyTable(['#'] + list(columnas))

        # Agregar filas a la 
            i=0
            for resultado in (resultados):
                tabla.add_row([i] + list(resultado.values()))
                i+=1

        # Devolver la tabla como string
            return [str(tabla),resultados]
        else:
            return "No se encontraron resultados."




    
    def comprobarNumPlazas(self,idactividadentidad):
            
            query="SELECT COUNT(*) from Inscripciones where idactividadentidad = ?"
            numplazasocupadas=self.db.executeQuery(query,(idactividadentidad,))
            numplazasocupadas=numplazasocupadas[0]['COUNT(*)']
            query="SELECT plazas from ActividadEntidades where idactividadentidad= ?"
            numplazas=self.db.executeQuery(query,(idactividadentidad,))
            numplazas=numplazas[0]['plazas']
            if numplazas-numplazasocupadas<=0:
                return False
            else:
                return True
            
    def comprobarCorreo(self,correo,idactividad):
        query="SELECT COUNT(*) from Inscripciones where correo_electronico= ? and idactividadentidad=?"
        s=self.db.executeQuery(query,(correo,idactividad))
        s=s[0]['COUNT(*)']
        if s!=0:
            return False
        else:
            return True
        
    def comprobarMetPago(self,correo):
        query="SELECT IBAN, Numero_tarjeta, fecha_caducidad,CVV from Atletas where correo_electronico=?"
        s=self.db.executeQuery(query,(correo,))
        for clave in s[0]:
            valor=s[0][clave]
            if valor==None:
                return False
            else:
                return True
            
    def generar_justificante(self,idactividad,correo):
        query="SELECT nombre from Atletas where correo_electronico=?"
        nombre=self.db.executeQuery(query,(correo,))
        query="SELECT nombre_entidad, nombre_activ_entidad ,fecha ,hora_inicio,lugar,info_adicional from ActividadEntidades where idactividadentidad=? " 
        info_ent=self.db.executeQuery(query,(idactividad,))
        nombre=nombre[0]['nombre']
        nombre_entidad=info_ent[0]['nombre_entidad']
        nombre_activ=info_ent[0]['nombre_activ_entidad']
        fecha=info_ent[0]['fecha']
        hora=info_ent[0]['hora_inicio']
        lugar=info_ent[0]['lugar']
        info=info_ent[0]['info_adicional']
        with open('Justificante.txt', 'w') as file: 
            file.write(f"Estimado {nombre},\nDesde {nombre_entidad} te confirmamos tu incripcion a la actividad {nombre_activ}.\n  FECHA: {fecha},\n  HORA:  {hora},\n  LUGAR: {lugar}, \n{info}")            

    def registrar_inscripcion(self,correo_electronico,actividad_externa):
        nombre_actividad=actividad_externa['nombre_activ_entidad']
        nombre_actividad=str(nombre_actividad)
        query = "SELECT idactividadentidad from ActividadEntidades WHERE nombre_activ_entidad=?"
        idactividad=self.db.executeQuery(query,[nombre_actividad],)
        idactividad=idactividad[0]
        idactividad=idactividad['idactividadentidad']
        correo_electronico=str(correo_electronico)
        
        s=self.comprobarCorreo(correo_electronico,idactividad)
        if s==True:
            a=self.comprobarNumPlazas(idactividad)
            if a==True:
                l=self.obtenerTipoAtleta(correo_electronico)
                if l=="Free":
                    n=self.comprobarMetPago(correo_electronico)
                    if n==False:
                        print("MÉTODO DE PAGO NO VÁLIDO, ACTUALICE SU MÉTODO DE PAGO")
                    else:
                        query = """INSERT INTO Inscripciones(correo_electronico, idactividadentidad)VALUES (?, ?)"""
                        self.db.executeQuery(query, (correo_electronico, idactividad))
                        print("se ha registrado la inscripcion")
                        self.generar_justificante(idactividad,correo_electronico)
                else:
                    query = """INSERT INTO Inscripciones(correo_electronico, idactividadentidad)VALUES (?, ?)"""
                    self.db.executeQuery(query, (correo_electronico, idactividad))
                    print("se ha registrado la inscripcion")
                    self.generar_justificante(idactividad,correo_electronico)
            else:
                print("NO QUEDAN PLAZAS DISPONIBLES")
        else:
            print("USUARIO YA REGISTRADO EN LA ACTIVIDAD")
            

    
   

    def obtenerTipoAtleta(self,correo_electronico):
        query = "SELECT tipo_atleta FROM Atletas WHERE correo_electronico = ?"
        resultado = self.db.executeQuery(query, (correo_electronico,))

        # Devuelve el tipo del atleta si se encuentra en la base de datos
        return resultado[0]['tipo_atleta'] if resultado else None
    
    def cambiarTipoAtleta(self, correo_electronico):
        # Obtener el tipo actual del atleta
        tipo_actual = self.obtenerTipoAtleta(correo_electronico)

        # Si no se encuentra el atleta, imprimir un mensaje de error
        if tipo_actual is None:
            print("No se encontró un atleta con ese correo electrónico.")
            return

        # Determinar el nuevo tipo
        nuevo_tipo = 'Premium' if tipo_actual == 'Free' else 'Free'

        print(f"¡Cambiando de '{tipo_actual}' a '{nuevo_tipo}'!")

        # Obtener la conexión a la base de datos
        db = DataBase("deporte.db")

        try:
            # Si el nuevo tipo es 'Premium', solicitar información adicional
            if nuevo_tipo == 'Premium':
                iban = input("Ingrese su IBAN: ")
                num_tarjeta = input("Ingrese su número de tarjeta: ")
                fecha_caducidad = input("Ingrese la fecha de caducidad de su tarjeta (mm/yy): ")
                cvv = input("Ingrese el CVV de su tarjeta: ")

                # Actualizar la información en la base de datos
                query = """
                    UPDATE Atletas
                    SET tipo_atleta = ?, IBAN = ?, Numero_tarjeta = ?, fecha_caducidad = ?, CVV = ?
                    WHERE correo_electronico = ?
                """
                db.executeUpdateQuery(query, nuevo_tipo, iban, num_tarjeta, fecha_caducidad, cvv, correo_electronico)

            # Si el nuevo tipo es 'Free', eliminar información adicional
            else:
                # Actualizar la información en la base de datos eliminando los valores
                query = """
                    UPDATE Atletas
                    SET tipo_atleta = ?, IBAN = NULL, Numero_tarjeta = NULL, fecha_caducidad = NULL, CVV = NULL
                    WHERE correo_electronico = ?
                """
                db.executeUpdateQuery(query, nuevo_tipo, correo_electronico)

            print(f"¡Cambio de tipo exitoso! Ahora eres '{nuevo_tipo}'.")

        except Exception as e:
            print(f"Error durante el cambio de tipo: {e}")
    
    def obtenerTiposActividades(self, correo_electronico):
            query = "SELECT DISTINCT(nombre_subtipo) FROM Actividades WHERE correo_electronico = ?"
            tipos_actividades = self.db.executeQuery(query, (correo_electronico,))
            
            # Convierte la lista de resultados a una lista de tipos
            return [tipo['nombre_subtipo'] for tipo in tipos_actividades] 
    
    def obtenerdatosInscripción(self, correo_electronico):
        query = """SELECT ae.nombre_activ_entidad AS nombre_actividad, ae.fecha, ae.hora_inicio,
            ae.lugar, ae.coste_UsFree AS cuota, A.tipo_atleta
            FROM ActividadEntidades ae INNER JOIN Inscripciones i ON ae.idactividadentidad = i.idactividadentidad
            INNER JOIN Atletas A ON i.correo_electronico = A.correo_electronico
            WHERE A.correo_electronico=?
        """
        return self.db.executeQuery(query, (correo_electronico,))
    
    def atletasEnRango(self,fecha_nacimiento_maxima, fecha_nacimiento_minima):
        query = """
            SELECT correo_electronico, nombre, apellidos, fecha_nacimiento
            FROM Atletas
            WHERE fecha_nacimiento BETWEEN ? AND ?
        """
        atletas_en_rango = self.db.executeQuery(query, (fecha_nacimiento_maxima, fecha_nacimiento_minima))
        return atletas_en_rango 

    def obtenerFechaNacimientoAtleta(self, correo_electronico):
        query = "SELECT fecha_nacimiento FROM Atletas WHERE correo_electronico = ?"
        result = self.db.executeQuery(query, (correo_electronico,))
        return result

    def calcularEdadEnFecha(self, fecha_nacimiento, fecha_referencia):
        # Calcular la diferencia de años entre dos fechas
        diferencia_fechas = relativedelta(fecha_referencia, fecha_nacimiento)
        return diferencia_fechas.years

    def obtenerDatosAtleta(self, correo_electronico):
        query = "SELECT sexo FROM Atletas WHERE correo_electronico = ?"
        result = self.db.executeQuery(query, (correo_electronico,))

        if result:
            return {
                'sexo': result[0].get('sexo')
            }
        else:
            return None  
    

