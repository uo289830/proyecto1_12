import sys
from gestores.GestorModel import GestorModel
from actividades.ActividadModel import ActividadModel
from tabulate import tabulate
from datetime import datetime

class GestorView:
    
    def __init__(self):
        self.gestor = GestorModel()
        self.choices = { 
            "1": self.mostrarEstadoForma,
            "2": self.mostrarDeportistasMasActivos,
            "3": self.inscripciones,
            "4": self
        }
        
    def displayMenu(self):
        print(""" Opciones: \n
              1.- Mostrar el estado de forma \n
              2.- Obtener deportistas más activos por tipo de actividad
              3.- Mostrar inscripciones
              4.- Volver al menu principal
              """)
        
    def run(self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if action:
                if choice=="4":
                    return
                action()
            else:
                print("{0} no es una opción válida".format(choice))
                
    def mostrarEstadoForma(self):
        correos=self.actividad.correovalido()
        while True:
            correo_electronico = input("Correo electrónico del atleta:")
            if correo_electronico in correos:
                break
            else:
                print("No existe usuario con este email")
        estado_de_forma = self.gestor.calcularEstadoForma(correo_electronico)
        if estado_de_forma < 1:
            print("Estado de forma malo")
        elif estado_de_forma == 1:
            print("Buena forma")
        else:
            print("Muy buena forma")

    def mostrarDeportistasMasActivos(self):
        tipo_actividad = input("Introduce el tipo de actividad: ")
        atletas_activos = self.gestor.obtenerDeportistasMasActivos(tipo_actividad)
        
        if atletas_activos:
            print("Atletas más activos en el tipo de actividad '{}':".format(tipo_actividad))
            # Crear una lista de listas para usar en tabulate
            tabla_atletas = [
                [atleta['nombre_atleta'], atleta['fecha_alta'], atleta['total_actividades']] 
                for atleta in atletas_activos
            ]
            # Encabezados de la tabla
            headers = ["Nombre de usuario", "Fecha de Alta", "Total de Actividades"]
            # Imprimir la tabla
            print(tabulate(tabla_atletas, headers=headers, tablefmt="grid"))
        else:
            print("No se encontraron atletas activos para el tipo de actividad '{}'".format(tipo_actividad))
    

    def inscripciones(self):
        res = self.gestor.obtener_num_deportistas_inscritos()

        if res:
            print("Tabla de Inscripciones:")
            inscripciones_table = [["Nombre de la Entidad", "Nombre de la Actividad", "Fecha de la Actividad", "Número de Inscritos"]]

            fecha_actual = datetime.now()  # Fecha y hora actuales

            for inscripcion in res:
                entidad = inscripcion['nombre_entidad']
                actividad = inscripcion['nombre_activ_entidad']
                fecha_actividad_str = inscripcion['fecha']  # Ajusta según el nombre real de tu campo de fecha
                num_inscritos = inscripcion['num_inscritos']

                try:
                    # Convierte la cadena de fecha a un objeto datetime
                    fecha_actividad = datetime.strptime(fecha_actividad_str, "%Y-%m-%d")

                    # Compara las fechas
                    if fecha_actividad > fecha_actual:
                        inscripciones_table.append([entidad, actividad, fecha_actividad_str, num_inscritos])

                except ValueError as e:
                    print(f"Error al procesar la fecha: {e}. Fecha: {fecha_actividad_str}")

            print(tabulate(inscripciones_table, headers="firstrow", tablefmt="grid"))
        else:
            print("No hay inscripciones disponibles.")

    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0)