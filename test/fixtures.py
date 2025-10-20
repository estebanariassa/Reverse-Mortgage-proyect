import unittest
import psycopg2
import sys
import os
from psycopg2 import Error

# Agregar el directorio raíz al path para importar Secret_config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT

class TestFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.connection = psycopg2.connect(
                host=PGHOST,
                database=PGDATABASE,
                user=PGUSER,
                password=PGPASSWORD,
                port=PGPORT
            )
            cls.cursor = cls.connection.cursor()
        except (Exception, Error) as error:
            print("Error conectando a PostgreSQL:", error)
            raise

    def test_create_tables(self):
        """Test para crear todas las tablas necesarias"""
        try:
            # Crear tabla de clientes (clientess)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientess (
                    cedula VARCHAR(20) PRIMARY KEY NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    edad INTEGER NOT NULL CHECK (edad BETWEEN 65 AND 90),
                    direccion VARCHAR(100),
                    telefono VARCHAR(20),
                    correo VARCHAR(100),
                    fecha_registro DATE DEFAULT CURRENT_DATE
                )
            """)

            # Crear tabla de propiedades
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS propiedades (
                    codigo_propiedad SERIAL PRIMARY KEY,
                    cedula_cliente VARCHAR(20) NOT NULL,
                    valor_propiedad NUMERIC(15,2),
                    direccion VARCHAR(100),
                    area NUMERIC(10,2),
                    tipo VARCHAR(30)
                )
            """)

            # Crear tabla de hipotecas
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS hipotecas (
                    id_hipoteca SERIAL PRIMARY KEY,
                    codigo_propiedad VARCHAR(20) NOT NULL,
                    porcentaje_prestamo NUMERIC(5,2) NOT NULL CHECK (porcentaje_prestamo BETWEEN 0 AND 100),
                    tasa_interes NUMERIC(5,2) NOT NULL CHECK (tasa_interes BETWEEN 0 AND 100),
                    plazo_anios INTEGER NOT NULL CHECK (plazo_anios > 0),
                    renta_mensual NUMERIC(12,2),
                    deuda_final NUMERIC(14,2),
                    fecha_inicio DATE DEFAULT CURRENT_DATE,
                    fecha_fin DATE,
                    estado VARCHAR(20) DEFAULT 'ACTIVA'
                )
            """)

            # Crear tabla de herederos
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS herederos (
                    id_heredero SERIAL PRIMARY KEY,
                    cedula_cliente VARCHAR(20) NOT NULL,
                    nombre VARCHAR(50) NOT NULL,
                    relacion VARCHAR(30),
                    telefono VARCHAR(20),
                    correo VARCHAR(50)
                )
            """)

            self.connection.commit()
            self.assertTrue(True, "Tablas creadas exitosamente")

        except (Exception, Error) as error:
            self.fail(f"Error creando las tablas: {error}")

    @classmethod
    def tearDownClass(cls):
        if cls.connection:
            cls.cursor.close()
            cls.connection.close()

if __name__ == '__main__':
    unittest.main()