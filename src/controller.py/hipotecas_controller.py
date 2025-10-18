import psycopg2
from model.hipoteca import Hipoteca  

DB_CONFIG = {
    "host": "localhost",
    "database": "tu_basedatos",
    "user": "postgres",
    "password": "tu_contraseña"
}

class HipotecasController:

    @staticmethod
    def conectar():
        """Conecta a la base de datos PostgreSQL"""
        return psycopg2.connect(**DB_CONFIG)

 

    @staticmethod
    def crear_tabla():
        """Crea la tabla hipotecas si no existe"""
        conexion = HipotecasController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
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
            );
        """)
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar_tabla():
        """Elimina la tabla hipotecas"""
        conexion = HipotecasController.conectar()
        cursor = conexion.cursor()
        cursor.execute("DROP TABLE IF EXISTS hipotecas;")
        conexion.commit()
        conexion.close()

    # ---------------------------------------------------------
    # INSERTAR HIPOTECA
    # ---------------------------------------------------------

    @staticmethod
    def insertar(hipoteca: Hipoteca):
        """Inserta una hipoteca en la base de datos"""
        conexion = HipotecasController.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO hipotecas 
                (codigo_propiedad, porcentaje_prestamo, tasa_interes, plazo_anios, renta_mensual, deuda_final, fecha_inicio, fecha_fin, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (hipoteca.codigo_propiedad, hipoteca.porcentaje_prestamo, hipoteca.tasa_interes,
                  hipoteca.plazo_anios, hipoteca.renta_mensual, hipoteca.deuda_final,
                  hipoteca.fecha_inicio, hipoteca.fecha_fin, hipoteca.estado))
            conexion.commit()
            return True
        except psycopg2.IntegrityError as e:
            conexion.rollback()
            print(f"Error de integridad: {e}")
            raise
        except Exception as e:
            conexion.rollback()
            print(f"Error al insertar hipoteca: {e}")
            raise
        finally:
            conexion.close()

    
    @staticmethod
    def buscar(id_hipoteca):
        """Busca una hipoteca por ID"""
        conexion = HipotecasController.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM hipotecas WHERE id_hipoteca = %s;", (id_hipoteca,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Hipoteca(*fila)
        return None
