import unittest
import sys
sys.path.append("src")

from model.clientes import Cliente
from ontroller.clientes_controller import ClientesController


class TestCliente(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se ejecuta antes de las pruebas"""
        ClientesController.borrar_tabla()
        ClientesController.crear_tabla()

    def test_insert_cliente(self):
        """Prueba insertar un cliente válido"""
        cliente = Cliente(
            cedula="1234567890",
            nombre="Carlos Gómez",
            edad=70,
            direccion="Calle 10 # 20-30",
            telefono="3124567890",
            correo="carlosgomez@example.com"
        )

        resultado = ClientesController.insertar(cliente)
        self.assertTrue(resultado, "El cliente no se insertó correctamente")

        buscado = ClientesController.buscar("1234567890")
        self.assertIsNotNone(buscado, "No se encontró el cliente insertado")
        self.assertEqual(buscado.nombre, "Carlos Gómez")

    def test_edad_invalida(self):
        """Prueba que no se pueda insertar un cliente con edad fuera del rango"""
        cliente = Cliente(
            cedula="9999999999",
            nombre="Persona Invalida",
            edad=50,  # fuera del rango permitido (65-90)
            direccion="Calle Falsa 123",
            telefono="3000000000",
            correo="falso@example.com"
        )
        with self.assertRaises(Exception):
            ClientesController.insertar(cliente)

    def test_buscar_inexistente(self):
        """Prueba buscar un cliente que no existe"""
        resultado = ClientesController.buscar("0000000000")
        self.assertIsNone(resultado, "Debería devolver None si no existe")

if __name__ == "__main__":
    unittest.main()
