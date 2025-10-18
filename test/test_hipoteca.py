import unittest
from controller.hipotecas_controller import HipotecasController
from model.hipoteca import Hipoteca
from datetime import date, timedelta

class TestHipotecasController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se ejecuta una sola vez al inicio: crea la tabla"""
        HipotecasController.borrar_tabla()
        HipotecasController.crear_tabla()

    def setUp(self):
        """Se ejecuta antes de cada test: limpia e inserta datos base"""
        HipotecasController.borrar_tabla()
        HipotecasController.crear_tabla()

        self.hipoteca_base = Hipoteca(
            id_hipoteca=None,
            codigo_propiedad="PROP001",
            porcentaje_prestamo=60.0,
            tasa_interes=10.5,
            plazo_anios=15,
            renta_mensual=2500000.0,
            deuda_final=450000000.0,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=15 * 365),
            estado="ACTIVA"
        )

    def test_insertar_hipoteca(self):
        """Prueba la inserción de una hipoteca"""
        resultado = HipotecasController.insertar(self.hipoteca_base)
        self.assertTrue(resultado, "No se pudo insertar la hipoteca correctamente")

    def test_buscar_hipoteca(self):
        """Prueba la búsqueda de una hipoteca por ID"""
        HipotecasController.insertar(self.hipoteca_base)

        # Recuperar la primera hipoteca insertada
        conexion = HipotecasController.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_hipoteca FROM hipotecas LIMIT 1;")
        id_hipoteca = cursor.fetchone()[0]
        conexion.close()

        hipoteca = HipotecasController.buscar(id_hipoteca)
        self.assertIsNotNone(hipoteca, "No se encontró la hipoteca insertada")
        self.assertEqual(hipoteca.codigo_propiedad, "PROP001")
        self.assertEqual(hipoteca.estado, "ACTIVA")

    def test_validacion_tasa_interes_invalida(self):
        """Prueba que falle si se inserta una tasa fuera del rango permitido"""
        hipoteca_invalida = Hipoteca(
            id_hipoteca=None,
            codigo_propiedad="PROP002",
            porcentaje_prestamo=50.0,
            tasa_interes=150.0,  # fuera del rango
            plazo_anios=10,
            renta_mensual=2000000.0,
            deuda_final=300000000.0,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=10 * 365),
            estado="ACTIVA"
        )

        with self.assertRaises(Exception):
            HipotecasController.insertar(hipoteca_invalida)

if __name__ == '__main__':
    unittest.main()
