import sys
sys.path.append("src")

import unittest
from model.calculadora import Calculadora, EdadInvalidaException

class HipotecaInversaTest(unittest.TestCase):
    """
    Unit Tests para la clase Calculadora del proyecto Hipoteca Inversa.

    Pruebas unitarias que validan el cálculo del monto mensual, deuda total y
    validaciones de edad según las reglas del sistema.
    """

    def test_calculo_basico(self):
        """Caso base: cálculo con valores normales."""
        valor_vivienda = 200000000   
        porcentaje_prestamo = 40    
        edad = 70                   
        pago_mensual_esperado = 600000
        deuda_total_esperada = 210000000

        resultado = Calculadora.calcular_hipoteca(valor_vivienda, porcentaje_prestamo, edad)
        pago_mensual = resultado["pago_mensual"]
        deuda_total = resultado["deuda_total"]

        self.assertEqual(round(pago_mensual, 0), pago_mensual_esperado)
        self.assertEqual(round(deuda_total, 0), deuda_total_esperada)

    def test_edad_minima_invalida(self):
        """Verifica que se lance excepción si la edad es menor al mínimo permitido."""
        valor_vivienda = 150000000
        porcentaje_prestamo = 50
        edad = 60  

        self.assertRaises(EdadInvalidaException,
                          Calculadora.calcular_hipoteca,
                          valor_vivienda, porcentaje_prestamo, edad)

    def test_prestamo_sin_interes(self):
        """Prueba con tasa de interés cero."""
        valor_vivienda = 250000000
        porcentaje_prestamo = 50
        edad = 75

        resultado = Calculadora.calcular_hipoteca(valor_vivienda, porcentaje_prestamo, edad, interes=0)
        pago_mensual = resultado["pago_mensual"]

        self.assertGreater(pago_mensual, 0)
        self.assertIsInstance(pago_mensual, (int, float))

    def test_valores_limite(self):
        """Verifica el comportamiento con edad avanzada o préstamo alto."""
        valor_vivienda = 100000000
        porcentaje_prestamo = 90
        edad = 90

        resultado = Calculadora.calcular_hipoteca(valor_vivienda, porcentaje_prestamo, edad)
        self.assertLessEqual(resultado["deuda_total"], valor_vivienda * 1.5)

if __name__ == '__main__':
    unittest.main()

