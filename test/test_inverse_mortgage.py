import sys
sys.path.append("src")
import unittest
from model import calculadora


class TestInverseMortgage(unittest.TestCase):

    def test_renta_mensual_basica(self):
        propiedad = 200000000
        prestamo = 1.0   # 100% préstamo
        tasa = 10/100
        edad = 70   # plazo = 20 años (90 - 70)

        resultado = calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)
        
        renta_calculada = resultado["renta_mensual"]
        plazo = resultado["plazo"]

        self.assertEqual(plazo, 20)
        self.assertAlmostEqual(renta_calculada, 1930043.29, 2)


    def test_renta_mensual_otro(self):
        propiedad = 150000000
        prestamo = 0.8
        tasa = 11/100
        edad = 75  # plazo15años

        resultado = calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)

        renta_calculada = resultado["renta_mensual"]
        self.assertAlmostEqual(renta_calculada, 1363916.32, 2)


    def test_plazo_correcto(self):
        propiedad = 300000000
        prestamo = 1.0
        tasa = 9.5/100
        edad = 68  # plazo22años

        resultado = calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)

        self.assertEqual(resultado["plazo"], 22)
        self.assertTrue(resultado["deuda_final"] > 0)


    def test_Error_compra(self):
        propiedad = 0
        prestamo = 1.0
        tasa = 10/100
        edad = 70
        
        with self.assertRaises(calculadora.ErrorCompra):
            calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)


    def test_Error_tasa(self):
        propiedad = 200000000
        prestamo = 0.9
        tasa = 20/100   # fuera de rango (mayor a 12%)
        edad = 72

        with self.assertRaises(calculadora.ErrorTasa):
            calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)


    def test_Error_prestamo(self):
        propiedad = 120000000
        prestamo = 1.5  # más del 100%
        tasa = 10/100
        edad = 70
        
        with self.assertRaises(calculadora.ErrorPrestamo):
            calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)


    def test_Error_edad(self):
        propiedad = 100000000
        prestamo = 1.0
        tasa = 10/100
        edad = 60   # menor a 65 permitido
        
        with self.assertRaises(calculadora.ErrorEdad):
            calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)


    def test_Error_plazo(self):
        propiedad = 80000000
        prestamo = 1.0
        tasa = 9.5/100
        edad = 88   # plazo = 2 años (menor a 5 permitido)

        with self.assertRaises(calculadora.ErrorPlazo):
            calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)


    def test_recomendacion_vender(self):
        propiedad = 200000000
        prestamo = 0.5
        tasa = 10/100
        edad = 70

        resultado = calculadora.hipoteca_inversa(propiedad, prestamo, tasa, edad)
        
        self.assertIn("recomendacion", resultado)
        self.assertTrue("Conviene" in resultado["recomendacion"])


if __name__ == '__main__':
    unittest.main()
