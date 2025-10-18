import unittest
import sys
sys.path.append("src")

from model.propiedad import Propiedad
from controller.propiedades_controller import PropiedadesController

class TestPropiedad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PropiedadesController.borrar_tabla()
        PropiedadesController.crear_tabla()

    def test_insertar_y_buscar(self):
        # Crear propiedad
        propiedad = Propiedad(
            codigo_propiedad="P001",
            cedula_cliente="10101010",
            valor_propiedad=250000000,
            direccion="Calle 45 # 12-34",
            area=120.5,
            tipo="Apartamento"
        )

        # Insertar en la BD
        PropiedadesController.insertar(propiedad)

        # Buscar
        fila = PropiedadesController.buscar("P001")
        self.assertIsNotNone(fila)
        self.assertEqual(fila[0], "P001")
        self.assertEqual(fila[5], "Apartamento")

if __name__ == "__main__":
    unittest.main()
