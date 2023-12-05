import sys
from entidades.EntidadModel import EntidadModel

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
        while True:
            nombre_entidad=input("Nombre de la entidad:")
            s=self.actividad_ent.comprobarNomEnt(nombre_entidad)
            if s==True:
                break
            else:
                print("Nombre de Entidad no válido")
        while True:
            nombreActividad = input("Nombre de la actividad:")
            s=self.actividad_ent.comprobarNomActividad(nombreActividad)
            if s==True:
                break
            else:
                print("Nombre de la actividad no válido")
        descripcion=input("Breve descripcion de la actividad:")
        fecha = input("Fecha de la actividad (aaaa-mm-dd):")
        duracion = input("Duración de la actividad en días:")
        while True:
             hora=input("Hora de inicio de la actividad(hh:mm):")
             s=self.actividad_ent.comprobrarhora(hora) 
             if s==True:
                 break
             else:
                 print("Fecha de inicio inválida")                   
        localizacion = input("Lugar en el que se realizará la actividad:")
        plazas=input("Numero de plazas disponibles:")
        coste=input("Coste para usuarios FREE:")
        info=input("Información adicional acerca de la carrera o de gestion de inscripcion:")
       
        
        self.actividad_ent.insertActividadEntidad(nombre_entidad,nombreActividad,descripcion, fecha, duracion,hora, localizacion,plazas,coste,info)
        print("Actividad insertada")

    

    def verInscripcionesActividad(self):
        nombre_entidad = input("Ingrese el nombre de la entidad: ")
        actividades_entidad = self.actividad_ent.obtener_actividades_entidad(nombre_entidad)
        
        if actividades_entidad:
            print("Lista de Actividades:")
            for actividad in actividades_entidad:
                print(f"ID: {actividad['idactividadentidad']}, Nombre: {actividad['nombre_activ_entidad']}")

            id_seleccionado = int(input("Seleccione el ID de la actividad: "))
            
            resultados_inscripciones = self.actividad_ent.obtener_inscripciones(id_seleccionado)

            if resultados_inscripciones:
                print("Lista de Inscripciones:")
                for inscripcion in resultados_inscripciones:
                    print(f"Actividad: {inscripcion['nombre_actividad']}, Correo Electrónico: {inscripcion['correo_electronico']}, Tipo de Atleta: {inscripcion['tipo_atleta']}")
            else:
                print("No hay inscripciones disponibles para esta actividad.")
        else:
            print("No hay actividades disponibles para esta entidad.")    
    
    
    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0) 
