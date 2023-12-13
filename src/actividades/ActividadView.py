import sys
from actividades.ActividadModel import ActividadModel
from util.checkdate import DateChecker

class ActividadView:
    
    def __init__(self):
        self.actividad=ActividadModel()
        self.choices= { "1": self.nuevaActividad,
                         "2": self
                       }
        
           
    def displayMenu (self):
        print(""" Opciones: \n
              1.- Introducir una nueva actividad \n
              2.- Volver al menú principal
              """)
        
    #Muestra la lista de opciones y permite la selección
    def run (self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if action:
                if choice=="2":
                    return
                action()
            else:
                print("{0} no es una opción valida".format(choice))

    def nuevaActividad(self):
        while True:
            fecha = input("Fecha de la actividad (aaaa-mm-dd):")
         # Verifica si la fecha tiene el formato válido
            if not DateChecker.checkdate(fecha):
                print("Error: La fecha no tiene el formato válido (aaaa-mm-dd).")
            else:
                break
        
        while True:
            duracion = input("Duración de la actividad:")
            s=self.actividad.negs(duracion)
            if s==False:
                print("Duración inválida")
            else:
                break
        localizacion = input("Lugar en el que se realizó la actividad:")
        while True:
            distancia = input("Distancia recorrida:")
            s=self.actividad.negs(distancia)
            if s==False:
                print("Distancia inválida")
            else:
                break
        while True:
            FCmax = input("FCmax:")
            s=self.actividad.negs(FCmax)
            if s==False:
                print("FCMax inválida")
            else:
                break
        while True:
            FCmin = input("FCmin:")
            s=self.actividad.negs(FCmin)
            if s==False:
                print("FCMin inválida")
            else:
                break
        nombreActividad = input("Nombre de la categoria:")
        print("Actividades disponibles")
        actividades=self.actividad.actividades_disp()
        listaact=[]
        for actividad in actividades:
            listaact.append(actividad['nombre_subtipo'])
            
        while True:
            nombreSubtipo=input("Nombre de la actividad:")
            if nombreSubtipo in listaact:
                break
            else:
                print("Nombre de actividad inválido")
        correos=self.actividad.correovalido()
        while True:
            correo_electronico = input("Correo electrónico del atleta:")
            if correo_electronico in correos:
                break
            else:
                print("No existe usuario con este email")
        
        self.actividad.insertActividad(nombreActividad,nombreSubtipo, fecha, duracion, localizacion, distancia, FCmax, FCmin, correo_electronico)
        
    
    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0) 
        