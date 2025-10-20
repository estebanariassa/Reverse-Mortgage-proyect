import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
from model.propiedad import Propiedad

class PropiedadesController:
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
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            create table if not exists propiedades (
                codigo_propiedad serial primary key,
                cedula_cliente varchar(20) not null,
                valor_propiedad numeric(15,2),
                direccion varchar(100),
                area numeric(10,2),
                tipo varchar(30)
            );
        """)
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar_tabla():
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("drop table if exists propiedades;")
        conexion.commit()
        conexion.close()


    @staticmethod
    def insertar(propiedad: Propiedad):
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            insert into propiedades (codigo_propiedad, cedula_cliente, valor_propiedad, direccion, area, tipo)
            values (%s, %s, %s, %s, %s, %s);
        """, propiedad.to_tuple())
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(codigo_propiedad):
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("select * from propiedades where codigo_propiedad = %s;", (codigo_propiedad,))
        fila = cursor.fetchone()
        conexion.close()
        return fila

    @staticmethod
    def listar(limit=1000):
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            select codigo_propiedad, cedula_cliente, valor_propiedad, direccion, area, tipo
            from propiedades
            limit %s;
        """, (limit,))
        filas = cursor.fetchall()
        conexion.close()
        return filas
