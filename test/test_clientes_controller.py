import unittest
from unittest.mock import patch
import sys
sys.path.append("src")

from model.clientes import Cliente
from controller.clientes_controller import ClientesController

class TestClientesController(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.cliente_prueba = Cliente(
            cedula="1234567890",
            nombre="Carlos Gómez",
            edad=70,
            direccion="Calle 10 # 20-30",
            telefono="3124567890",
            correo="carlosgomez@example.com"
        )

    @patch('psycopg2.connect')
    def test_insertar_cliente(self, mock_connect):
        """Prueba insertar un cliente"""
        mock_cursor = mock_connect.return_value.cursor.return_value
        
        # Prueba inserción exitosa
        resultado = ClientesController.insertar(self.cliente_prueba)
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called_once()
        
    @patch('psycopg2.connect')
    def test_buscar_cliente(self, mock_connect):
        """Prueba buscar un cliente"""
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (
            "1234567890", "Carlos Gómez", 70,
            "Calle 10 # 20-30", "3124567890", "carlosgomez@example.com"
        )
        
        cliente = ClientesController.buscar("1234567890")
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.cedula, "1234567890")
        
    @patch('psycopg2.connect')
    def test_actualizar_cliente(self, mock_connect):
        """Prueba actualizar un cliente"""
        mock_cursor = mock_connect.return_value.cursor.return_value
        
        self.cliente_prueba.nombre = "Carlos Gómez Actualizado"
        resultado = ClientesController.actualizar(self.cliente_prueba)
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called_once()
        
    @patch('psycopg2.connect')
    def test_eliminar_cliente(self, mock_connect):
        """Prueba eliminar un cliente"""
        mock_cursor = mock_connect.return_value.cursor.return_value
        
        resultado = ClientesController.eliminar("1234567890")
        self.assertTrue(resultado)
        mock_cursor.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()