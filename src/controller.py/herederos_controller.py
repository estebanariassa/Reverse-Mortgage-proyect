import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
from model.heredero import Heredero

class HerederosController:
    @staticmethod
    def conectar():
        return psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            port=PGPORT
        )


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

    @staticmethod
    def insertar(heredero: Heredero):
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
        conexion = HerederosController.conectar()
        cursor = conexion.cursor()
        cursor.execute("select * from herederos where id_heredero = %s;", (id_heredero,))
        fila = cursor.fetchone()
        conexion.close()
        return fila

    @staticmethod
    def listar(limit=1000):
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
