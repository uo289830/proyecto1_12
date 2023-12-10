--Carga inicial de datos para pruebas

--Tabla Atletas
-- Insertar usuarios "Free"
INSERT INTO Atletas(correo_electronico, nombre, apellidos, fecha_alta, fecha_nacimiento, peso, altura, tipo_atleta, sexo)
VALUES ('Juan@gmail.com', 'Juan', 'Martinez', '2023-01-29', '1990-05-15', '70', '175', 'Free', 'Masculino');


-- Insertar usuarios "Premium" con valores para los campos adicionales
INSERT INTO Atletas(correo_electronico, nombre, apellidos, fecha_alta, fecha_nacimiento, peso, altura, tipo_atleta, IBAN, Numero_tarjeta, fecha_caducidad, CVV, sexo)
VALUES 
  ('Javier@gmail.com', 'Javier', 'Fernandez', '2023-01-29', '1985-12-10', '75', '180', 'Premium', 'ES12345678901234567890', '1234 5678 9012 3456', '01/25', '123', 'Masculino'),
  ('Marta@gmail.com', 'Marta', 'Puente', '2023-01-29', '1988-07-22', '65', '165', 'Premium', 'ES23456789012345678901', '2345 6789 0123 4567', '02/26', '456', 'Femenino'),
  ('Samuel@gmail.com', 'Samuel', 'Valle', '2023-01-29', '1992-03-05', '80', '185', 'Premium', 'ES34567890123456789012', '3456 7890 1234 5678', '03/23', '789', 'Masculino'),
  ('Sofia@gmail.com', 'Sofia', 'Rodriguez', '2023-01-29', '1995-09-18', '60', '170', 'Premium', 'ES45678901234567890123', '4567 8901 2345 6789', '04/24', '012', 'Femenino');


--Tabla Subtipos
insert into Subtipos(nombre_subtipo, met) values ('bicicleta montania', 8.5);
insert into Subtipos(nombre_subtipo, met) values ('bicicleta de paseo', 4.0);
insert into Subtipos(nombre_subtipo, met) values ('bicicleta de carretera', 10.0);
insert into Subtipos(nombre_subtipo, met) values ('caminar de paseo', 2.5);
insert into Subtipos(nombre_subtipo, met) values ('caminar rápido',5.0);
insert into Subtipos(nombre_subtipo, met) values ('senderismo',5.5);
insert into Subtipos(nombre_subtipo, met) values ('nadar a braza',10.0);
insert into Subtipos(nombre_subtipo, met) values ('nadar a crawl',10.5);
insert into Subtipos(nombre_subtipo, met) values ('nadar a espalda',7);
insert into Subtipos(nombre_subtipo, met) values ('nadar a mariposa',11.0);
insert into Subtipos(nombre_subtipo, met) values ('nadar',6.0);
insert into Subtipos(nombre_subtipo, met) values ('correr(8km/h)',8.0);
insert into Subtipos(nombre_subtipo, met) values ('correr(16km/h)',16.0);
insert into Subtipos(nombre_subtipo, met) values ('baile',4.89);
insert into Subtipos(nombre_subtipo, met) values ('aerobic',6.5);
insert into Subtipos(nombre_subtipo, met) values ('gym',5.5);
insert into Subtipos(nombre_subtipo, met) values ('calistenia',8);
insert into Subtipos(nombre_subtipo, met) values ('circuito',7);
insert into Subtipos(nombre_subtipo, met) values ('maquinaesqui',7);
insert into Subtipos(nombre_subtipo, met) values ('maquinaescalera',9);
insert into Subtipos(nombre_subtipo, met) values ('yoga',2.5);
insert into Subtipos(nombre_subtipo, met) values ('pilates',3);
insert into Subtipos(nombre_subtipo, met) values ('baseball',4);
insert into Subtipos(nombre_subtipo, met) values ('volleyball',4.5);
insert into Subtipos(nombre_subtipo, met) values ('baloncesto',6.5);
insert into Subtipos(nombre_subtipo, met) values ('futbol',7.0);
insert into Subtipos(nombre_subtipo, met) values ('waterpolo',10.0);
insert into Subtipos(nombre_subtipo, met) values ('rugby',8.5);
insert into Subtipos(nombre_subtipo, met) values ('cricket',5.0);
insert into Subtipos(nombre_subtipo, met) values ('caballo',5.5);
insert into Subtipos(nombre_subtipo, met) values ('patinar',6.0);
insert into Subtipos(nombre_subtipo, met) values ('golf',3.0);
insert into Subtipos(nombre_subtipo, met) values ('tenis',8.0);
insert into Subtipos(nombre_subtipo, met) values ('esquiar',7.5);
insert into Subtipos(nombre_subtipo, met) values ('comba',10.0);
insert into Subtipos(nombre_subtipo, met) values ('croquet',3.5);
insert into Subtipos(nombre_subtipo, met) values ('esgrima',6.0);
insert into Subtipos(nombre_subtipo, met) values ('boxeo',9.5);
insert into Subtipos(nombre_subtipo, met) values ('mma',10);

insert into Subtipos(nombre_subtipo, met) values ('kickboxing',7.5);

--artemarcial,individual,equipo,gimnasio,bailar,carrera,natacion,ciclismo,caminar

-- Tabla Actividades
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values( 'carrera', 'correr(8km/h)', '2023-8-13', 'parque', 45, 8, 120, 60, 'Javier@gmail.com');
insert into Actividades (nombre_actividad, nombre_subtipo, fecha, localizacion, duracion, distancia, FCmax, FCmin, correo_electronico) values ('ciclismo', 'bicicleta de paseo', '2023-4-14', 'ciudad', 90, 15, 160, 70, 'Marta@gmail.com');
insert into Actividades (nombre_actividad, nombre_subtipo, fecha, localizacion, duracion, distancia, FCmax, FCmin, correo_electronico) values ('baile', 'aerobic', '2023-1-15', 'carretera', 50, 0, 110, 68, 'Samuel@gmail.com');
insert into Actividades (nombre_actividad, nombre_subtipo, fecha, localizacion, duracion, distancia, FCmax, FCmin, correo_electronico) values('natacion', 'nadar a crawl', '2023-5-16', 'piscina', 45, 1, 101, 70, 'Sofia@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('ciclismo', 'bicicleta montania', '2023-2-11', 'montaña', 35, 20, 120, 60, 'Juan@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('ciclismo', 'bicicleta montania', '2023-3-13', 'montaña', 35, 20, 112, 65, 'Juan@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('senderismo', 'senderismo', '2023-03-14', 'bosque', 40, 15, 120, 60, 'javier@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('natacion', 'nadar a braza', '2023-03-15', 'piscina municipal', 60, 0, 106, 70, 'marta@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('correr', 'correr(8km/h)', '2023-03-16', 'parque', 30, 10, 140, 75, 'sofia@gmail.com');
insert into Actividades (nombre_actividad,nombre_subtipo,fecha,localizacion,duracion,distancia,FCmax,FCmin,correo_electronico) values('relajacion', 'yoga', '2023-03-17', 'estudio de yoga', 90, 0, 110, 55, 'samuel@gmail.com');
--Tabla ActividadEntidades
insert into ActividadEntidades (nombre_entidad, nombre_activ_entidad ,descripcion ,fecha ,duracion_dias,hora_inicio,lugar,plazas,coste_UsFree,info_adicional) values ('Runners SA','Maraton SA','Recorrido 30km por el centro de la ciudad','2023-12-31',1,'09:00','Valencia',1000,4.99,'Cualquier cambio sera notificado atraves de este medio');
insert into ActividadEntidades (nombre_entidad, nombre_activ_entidad ,descripcion ,fecha ,duracion_dias,hora_inicio,lugar,plazas,coste_UsFree,info_adicional) values ('Runners SA','Maraton Madrid SA','Recorrido 42km por el centro de la ciudad','2023-11-30',1,'10:00','Madrid',1000,5.99,'Cualquier cambio sera notificado atraves de este medio');
insert into ActividadEntidades (nombre_entidad, nombre_activ_entidad ,descripcion ,fecha ,duracion_dias,hora_inicio,lugar,plazas,coste_UsFree,info_adicional) values ('xx','xx','xx','2023-12-12',1,'00:00','xx',1,0,'xx');

--Tabla Inscripciones
insert into Inscripciones (correo_electronico, idactividadentidad) values ('Javier@gmail.com', 1);
insert into Inscripciones (correo_electronico, idactividadentidad) values ('Marta@gmail.com', 1);
insert into Inscripciones (correo_electronico, idactividadentidad) values ('Sofia@gmail.com', 1);
insert into Inscripciones (correo_electronico, idactividadentidad) values ('Juan@gmail.com', 1);