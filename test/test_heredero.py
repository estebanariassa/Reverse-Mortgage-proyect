import unittest
import sys
sys.path.append("src")

from model.heredero import Heredero
from controller.herederos_controller import HerederosController

class TestHeredero(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        HerederosController.borrar_tabla()
        HerederosController.crear_tabla()

    def test_insertar_y_buscar(self):
        heredero = Heredero(
            id_heredero=1,
            cedula_cliente="10101010",
            nombre="Carlos Gómez",
            relacion="Hijo",
            telefono="3214567890",
            correo="carlosgomez@gmail.com"
        )

        # Insertar en la base de datos
        HerederosController.insertar(heredero)

        # Buscar
        fila = HerederosController.buscar(1)
        self.assertIsNotNone(fila)
        self.assertEqual(fila[0], 1)
        self.assertEqual(fila[2], "Carlos Gómez")

if __name__ == "__main__":
    unittest.main()
