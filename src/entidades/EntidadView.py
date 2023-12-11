import sys
from entidades.EntidadModel import EntidadModel
from tabulate import tabulate
from datetime import datetime, timedelta
from util.checkdate import DateChecker 

class EntidadView:
    
    def __init__(self):
        self.actividad_ent=EntidadModel()
        self.choices= { "1": self.nuevaActividadEntidad,
                        "2":self.verInscripcionesActividad,
                        "3": self.quit
                       }
        
           
    def displayMenu (self):
        print(""" Opciones: \n
              1.- Introducir una nueva actividad \n
              2.- Ver inscripciones por actividad
              3.- Salir 
              """)
        
    #Muestra la lista de opciones y permite la selección
    def run (self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} no es una opción valida".format(choice))
    
    
    #Vista para la HU1 Insertar una actividad (Adriana)
    def nuevaActividadEntidad(self):
        nombre_entidad=input("Nombre de la entidad:")
        nombreActividad = input("Nombre de la actividad:")
        descripcion=input("Breve descripcion de la actividad:")
        while True:
            fecha = input("Fecha de la actividad (aaaa-mm-dd):")
            if not DateChecker.checkdateEntidad(fecha):
                print("La fecha no es válida.")
            else:
                break  
        duracion = input("Duración de la actividad en días:")
        while True:
             hora=input("Hora de inicio de la actividad(hh:mm):")
             s=self.actividad_ent.comprobrarhora(hora) 
             if s==True:
                 break
             else:
                 print("Fecha de inicio inválida")                   
        localizacion = input("Lugar en el que se realizará la actividad:")
        while True:
            plazas=input("Numero de plazas disponibles:")
            s=self.actividad_ent.plazasneg(plazas)
            if s==True:
                break
            else:
                print("Número de plazas inválido")
        while True:
            coste=input("Coste para usuarios FREE:")
            s=self.actividad_ent.costeneg(coste)
            if s==True:
                break
            else:
                print("Coste para ususarios Free inválido") 
        info=input("Información adicional acerca de la carrera o de gestion de inscripcion:")
       
        
        self.actividad_ent.insertActividadEntidad(nombre_entidad,nombreActividad,descripcion, fecha, duracion,hora, localizacion,plazas,coste,info)
        print("Actividad insertada")

    

    

    def verInscripcionesActividad(self):
        nombre_entidad = input("Ingrese el nombre de la entidad: ")
        actividades_entidad = self.actividad_ent.obtener_actividades_entidad(nombre_entidad)

        if actividades_entidad:
            print("Lista de Actividades:")
            actividades_table = [["ID", "Nombre"]]

            for actividad in actividades_entidad:
                actividades_table.append([actividad['idactividadentidad'], actividad['nombre_activ_entidad']])

            print(tabulate(actividades_table, headers="firstrow", tablefmt="grid"))

            id_seleccionado = int(input("Seleccione una de la actividad: "))
            resultados_inscripciones = self.actividad_ent.obtener_inscripciones(id_seleccionado)

            if resultados_inscripciones:
                print("Lista de Inscripciones:")
                inscripciones_table = [["Actividad", "Correo Electrónico", "Tipo de Atleta", "Cuota"]]

                for inscripcion in resultados_inscripciones:
                    tipo_atleta = inscripcion['tipo_atleta']
                    if tipo_atleta.lower() == 'free':
                        cuota = inscripcion['coste_UsFree']
                    else:
                        cuota = 0

                    inscripciones_table.append([inscripcion['nombre_actividad'], inscripcion['correo_electronico'], tipo_atleta, cuota])

                print(tabulate(inscripciones_table, headers="firstrow", tablefmt="grid"))
            else:
                print("No hay inscripciones disponibles para esta actividad.")
        else:
            print("No hay actividades disponibles para esta entidad.")

    
    
    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0) 
