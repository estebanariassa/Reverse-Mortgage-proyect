# Sistema de Hipoteca Inversa

Un sistema desarrollado para calcular y gestionar hipotecas inversas. Permite a los usuarios simular diferentes escenarios y administrar la información de clientes, propiedades e hipotecas.

## Instrucciones de Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

### Pasos para Instalar

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/estebanariassa/Reverse-Mortgage-proyect.git
   cd Reverse-Mortgage-proyect
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos PostgreSQL:**

   **Opción A: Base de datos local**
   - Instalar PostgreSQL en tu sistema
   - Crear una base de datos llamada `calculadora_de_hipoteca_inversa`
   - Configurar el archivo `Secret_config.py` con tus credenciales locales

   **Opción B: Base de datos en la nube (Render)**
   - La base de datos ya está configurada en Render
   - El archivo `Secret_config.py` ya contiene las credenciales necesarias

4. **Crear las tablas de la base de datos:**
   ```bash
   # Opción 1: Script automático de configuración (Recomendado)
   python setup_database.py
   
   # Opción 2: Ejecutar el script de creación de tablas
   python -m test.fixtures
   ```

5. **Ejecutar la aplicación:**
   ```bash
   # Interfaz gráfica con Kivy (Calculadora de hipoteca inversa)
   python src/view/interface.py
   
   # Interfaz de gestión de base de datos
   python src/view/database_interface.py
   
   # O ejecutar desde main.py
   python src/view/main.py
   ```

### Configuración del archivo Secret_config.py

El archivo `Secret_config.py` contiene las credenciales de conexión a la base de datos. **IMPORTANTE:** Este archivo contiene información sensible y no debe ser compartido públicamente.

**Estructura del archivo:**
```python
PGHOST='host_de_la_base_de_datos'
PGDATABASE='nombre_de_la_base_de_datos'
PGUSER='usuario_de_la_base_de_datos'
PGPASSWORD='contraseña_de_la_base_de_datos'
PGPORT=5432
```

**Para uso local:**
- Reemplaza los valores con tus credenciales de PostgreSQL local
- Asegúrate de que la base de datos `calculadora_de_hipoteca_inversa` exista

**Para uso en producción:**
- El archivo ya está configurado para la base de datos en Render
- No modifiques estos valores a menos que tengas una nueva base de datos

### Ejecución de Pruebas
Para ejecutar las pruebas unitarias:
```bash
python -m unittest discover test
```

### Funcionalidades del Sistema

#### 1. Calculadora de Hipoteca Inversa (`interface.py`)
- Simulación de hipoteca inversa
- Cálculo de renta mensual
- Validación de parámetros de entrada
- Interfaz gráfica intuitiva

#### 2. Gestión de Base de Datos (`database_interface.py`)
- **Gestión de Clientes**: Insertar, buscar y modificar datos de clientes
- **Gestión de Propiedades**: Administrar información de propiedades
- **Gestión de Hipotecas**: Controlar contratos de hipoteca inversa
- **Gestión de Herederos**: Gestionar información de herederos
- Interfaz gráfica completa con navegación entre módulos

#### 3. Casos de Prueba
- **Test Fixtures**: Creación automática de tablas
- **Casos de Inserción**: 3 casos de prueba para cada entidad
- **Casos de Modificación**: 3 casos de prueba para actualizar datos
- **Casos de Búsqueda**: 3 casos de prueba para consultar información

#### 4. Características Técnicas
- **Interfaz Gráfica**: Desarrollada con Kivy
- **Base de Datos**: PostgreSQL con operaciones CRUD
- **Validaciones**: Sistema de validación de datos
- **Pruebas**: Casos de prueba unitarios

---

## Estructura del Proyecto

```
src/
├── model/              # Modelos de datos
├── controller/         # Lógica de negocio
├── view/              # Interfaces de usuario
├── database/          # Gestión de BD
└── utils/             # Utilidades
```

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