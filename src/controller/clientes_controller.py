import os
import importlib.util


def _load_real_controller():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_path = os.path.join(base_dir, "controller.py", "clientes_controller.py")
    spec = importlib.util.spec_from_file_location("clientes_controller_real", real_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


_module = _load_real_controller()
ClientesController = getattr(_module, "ClientesController")

import psycopg2
from psycopg2 import Error
from model.clientes import Cliente

class ClientesController:
    @staticmethod
    def crear_tabla():
        """Crear la tabla de clientes si no existe"""
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="your_password",
                host="127.0.0.1",
                port="5432",
                database="hipoteca_inversa"
            )
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    cedula VARCHAR(20) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    edad INTEGER NOT NULL,
                    direccion VARCHAR(200),
                    telefono VARCHAR(20),
                    correo VARCHAR(100)
                )
            """)
            connection.commit()
            return True

        except (Exception, Error) as error:
            print(f"Error: {error}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def insertar(cliente):
        """Insertar un nuevo cliente"""
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="your_password",
                host="127.0.0.1",
                port="5432",
                database="hipoteca_inversa"
            )
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO clientes (cedula, nombre, edad, direccion, telefono, correo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cliente.cedula, cliente.nombre, cliente.edad, 
                  cliente.direccion, cliente.telefono, cliente.correo))
            
            connection.commit()
            return True

        except (Exception, Error) as error:
            print(f"Error: {error}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def buscar(cedula):
        """Buscar un cliente por cédula"""
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="your_password",
                host="127.0.0.1",
                port="5432",
                database="hipoteca_inversa"
            )
            cursor = connection.cursor()

            cursor.execute("""
                SELECT cedula, nombre, edad, direccion, telefono, correo
                FROM clientes WHERE cedula = %s
            """, (cedula,))
            
            resultado = cursor.fetchone()
            if resultado:
                return Cliente(
                    cedula=resultado[0],
                    nombre=resultado[1],
                    edad=resultado[2],
                    direccion=resultado[3],
                    telefono=resultado[4],
                    correo=resultado[5]
                )
            return None

        except (Exception, Error) as error:
            print(f"Error: {error}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def actualizar(cliente):
        """Actualizar un cliente existente"""
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="your_password",
                host="127.0.0.1",
                port="5432",
                database="hipoteca_inversa"
            )
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE clientes 
                SET nombre = %s, edad = %s, direccion = %s, telefono = %s, correo = %s
                WHERE cedula = %s
            """, (cliente.nombre, cliente.edad, cliente.direccion, 
                  cliente.telefono, cliente.correo, cliente.cedula))
            
            connection.commit()
            return True

        except (Exception, Error) as error:
            print(f"Error: {error}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def eliminar(cedula):
        """Eliminar un cliente"""
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="your_password",
                host="127.0.0.1",
                port="5432",
                database="hipoteca_inversa"
            )
            cursor = connection.cursor()

            cursor.execute("DELETE FROM clientes WHERE cedula = %s", (cedula,))
            connection.commit()
            return True

        except (Exception, Error) as error:
            print(f"Error: {error}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()