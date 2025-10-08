# Calculadora de Hipoteca Inversa

Este proyecto simula una **hipoteca inversa**, un producto financiero en el cual un banco entrega al propietario una renta mensual basada en el valor de su vivienda, sin necesidad de pagar cuotas durante el plazo del contrato.

---

## Descripción del Proyecto

- El banco entrega al propietario una **renta mensual** basada en el valor de su vivienda.
- El propietario **no paga cuotas mensuales** durante el contrato.
- Al fallecimiento del titular o al finalizar el plazo, la **deuda se liquida** con la venta de la propiedad o con recursos de los herederos.

---

## Entregas del Proyecto

### Entrega 1 y 2:

**Autores:**
- Esteban Arias Salazar y Nicol Valeria Atehortua

**Contribuciones:**
- Implementación del modelo base de la hipoteca inversa.
- Lógica de cálculo financiero.
- Pruebas unitarias iniciales.
- Mejoras en la lógica del sistema.
- Validación de entradas.
- Optimización del cálculo de la renta mensual y deuda final.

---

### Entrega 3:

**Autores:**
- Juan Manuel y Mateo Molina Gonzalez

**Contribuciones:**
- Desarrollo de una interfaz gráfica con **Kivy**.
- Instrucciones detalladas para clonar, ejecutar el proyecto y correr las pruebas.
- Mejora en la presentación de resultados.
- Refactorización de código para facilitar el uso y pruebas.

---

## Campos de Entrada

| Campo                     | Descripción                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Valor de la propiedad    | Precio de la vivienda (en COP)                                              |
| Porcentaje del préstamo  | Porcentaje del valor de la vivienda a prestar (0% - 100%)                   |
| Tasa de interés anual    | Entre 9% y 12%                                                              |
| Edad del propietario     | Entre 65 y 90 años                                                          |
| Plazo del contrato       | Calculado automáticamente como `90 - edad` (mínimo 5 años)                 |

---

## Salidas Generadas

| Campo                         | Descripción                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| Renta mensual (COP)          | Monto que recibe el propietario cada mes                                   |
| Plazo del contrato (años)    | Definido según la edad del propietario                                      |
| Monto total del préstamo     | Valor máximo prestado sobre la vivienda                                     |
| Deuda final acumulada (COP)  | Total que debe liquidarse al final del contrato                             |
| Recomendación del sistema    | Sugerencia entre vender o entregar la vivienda al banco                     |
| Opciones para herederos      | 1) Vender la vivienda  2) Pagar la deuda  3) Entregar la vivienda al banco  |

---

## Instrucciones para Clonar y Ejecutar

### 1. Clonar el repositorio

```bash
git clone https://github.com/estebanariassa/Reverse-Mortgage-proyect.git
```

### 2. Navegar al directorio del proyecto

```bash
cd Reverse-Mortgage-proyect
```

### 4. Ejecutar las pruebas unitarias

```bash
py test/test_inverse_mortgage.py
```

### 5. Ejecutar la interfaz gráfica (Kivy)

```bash
pip install kivymd
```

Esto abrirá la aplicación con la interfaz gráfica desarrollada en Kivy. Desde allí podrás ingresar los datos y simular la hipoteca inversa visualmente.
