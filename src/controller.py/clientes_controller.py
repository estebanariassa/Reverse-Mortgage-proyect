import psycopg2
import sys
import os

# Agregar el directorio raíz al path para importar Secret_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
from model.clientes import Cliente


DB_CONFIG = {
    "host": PGHOST,
    "database": PGDATABASE,
    "user": PGUSER,
    "password": PGPASSWORD,
    "port": PGPORT
}

class ClientesController:

    @staticmethod
    def conectar():
        """Conecta a la base de datos PostgreSQL"""
        return psycopg2.connect(**DB_CONFIG)

    @staticmethod
    def crear_tabla():
        """Crea la tabla clientess si no existe"""
        conexion = ClientesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientess (
                cedula VARCHAR(20) PRIMARY KEY NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                edad INTEGER NOT NULL CHECK (edad BETWEEN 65 AND 90),
                direccion VARCHAR(100),
                telefono VARCHAR(20),
                correo VARCHAR(100),
                fecha_registro DATE DEFAULT CURRENT_DATE
            );
        """)
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar_tabla():
        """Elimina la tabla clientess"""
        conexion = ClientesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("DROP TABLE IF EXISTS clientess;")
        conexion.commit()
        conexion.close()

    @staticmethod
    def insertar(cliente: Cliente):
        """Inserta un cliente en la base de datos"""
        conexion = ClientesController.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO clientess (cedula, nombre, edad, direccion, telefono, correo)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (cliente.cedula, cliente.nombre, cliente.edad,
                  cliente.direccion, cliente.telefono, cliente.correo))
            conexion.commit()
            return True
        except psycopg2.IntegrityError as e:
            conexion.rollback()
            print(f"Error de integridad: {e}")
            raise
        except Exception as e:
            conexion.rollback()
            print(f"Error al insertar cliente: {e}")
            raise
        finally:
            conexion.close()

    @staticmethod
    def buscar(cedula):
        """Busca un cliente por cédula"""
        conexion = ClientesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientess WHERE cedula = %s;", (cedula,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Cliente(*fila)
        return None
