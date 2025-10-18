create table if not exists clientess (
    cedula varchar(20) primary key not null,
    nombre varchar(50) not null,
    edad int not null check (edad between 65 and 90),
    direccion varchar(100),
    telefono varchar(20),
    correo varchar(50),
    fecha_registro date default current_date
);