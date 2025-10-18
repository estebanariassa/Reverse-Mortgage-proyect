import psycopg2
from model.heredero import Heredero

class HerederosController:
    @staticmethod
    def conectar():
        """
        Establece conexión con la base de datos PostgreSQL.
        Ajusta las credenciales según tu entorno.
        """
        return psycopg2.connect(
            host="localhost",
            database="ejemplo-db",
            user="postgres",
            password="tu_contraseña"
        )

    # -----------------------------------------------------------
    # Crear o eliminar tabla
    # -----------------------------------------------------------

    @staticmethod
    def crear_tabla():
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            create table if not exists herederos (
                id_heredero serial primary key,
                cedula_cliente varchar(20) not null,
                nombre varchar(50) not null,
                relacion varchar(30),
                telefono varchar(20),
                correo varchar(50)
            );
        """)
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar_tabla():
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()
        cursor.execute("drop table if exists herederos;")
        conexion.commit()
        conexion.close()

    # -----------------------------------------------------------
    # Operaciones CRUD
    # -----------------------------------------------------------

    @staticmethod
    def insertar(heredero: Heredero):
        """
        Inserta un heredero en la base de datos.
        Si el id_heredero es None, se genera automáticamente (serial).
        """
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()

        if heredero.id_heredero is None:
            cursor.execute("""
                insert into herederos (cedula_cliente, nombre, relacion, telefono, correo)
                values (%s, %s, %s, %s, %s)
                returning id_heredero;
            """, (heredero.cedula_cliente, heredero.nombre, heredero.relacion,
                  heredero.telefono, heredero.correo))
            heredero.id_heredero = cursor.fetchone()[0]
        else:
            cursor.execute("""
                insert into herederos (id_heredero, cedula_cliente, nombre, relacion, telefono, correo)
                values (%s, %s, %s, %s, %s, %s);
            """, heredero.to_tuple())

        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(id_heredero):
        """
        Busca un heredero por su ID.
        """
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()
        cursor.execute("select * from herederos where id_heredero = %s;", (id_heredero,))
        fila = cursor.fetchone()
        conexion.close()
        return fila

    @staticmethod
    def listar(limit=1000):
        """
        Lista todos los herederos hasta un límite especificado.
        """
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            select id_heredero, cedula_cliente, nombre, relacion, telefono, correo
            from herederos
            limit %s;
        """, (limit,))
        filas = cursor.fetchall()
        conexion.close()
        return filas
