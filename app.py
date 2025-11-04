
from flask import Flask    


from flask import render_template, request

import sys
import os
import importlib.util

sys.path.append("src")


def cargar_controlador(nombre_archivo, nombre_clase):
    """Carga un controlador desde el directorio controller.py"""
    directorio_base = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio_base, "src", "controller.py", nombre_archivo)
    
    if not os.path.exists(ruta_archivo):
        raise ImportError(f"No se encontró el archivo: {ruta_archivo}")
    

    if directorio_base not in sys.path:
        sys.path.insert(0, directorio_base)
    
    spec = importlib.util.spec_from_file_location(nombre_archivo.replace(".py", ""), ruta_archivo)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el módulo {nombre_archivo}")
    
    module = importlib.util.module_from_spec(spec)

    module.__file__ = os.path.abspath(ruta_archivo)
    spec.loader.exec_module(module)
    return getattr(module, nombre_clase)


ClientesController = cargar_controlador("clientes_controller.py", "ClientesController")
PropiedadesController = cargar_controlador("propiedades_controller.py", "PropiedadesController")
HipotecasController = cargar_controlador("hipotecas_controller.py", "HipotecasController")
HerederosController = cargar_controlador("herederos_controller.py", "HerederosController")


from model.clientes import Cliente
from model.propiedad import Propiedad
from model.hipoteca import Hipoteca
from model.heredero import Heredero


app = Flask(__name__, template_folder='src/templates')     


@app.route('/')      
def hello():
    return render_template("hipotecas.html")

@app.route('/buscar_datos')
def buscar_datos():
    return render_template("buscar_datos.html")

@app.route('/guardar_cliente')
def guardar_cliente():
    # Crear un cliente
    cliente = Cliente(cedula="", nombre="", edad=0, direccion="", telefono="", correo="")
    cliente.cedula = request.args["cedula"]
    cliente.nombre = request.args["nombre"]
    cliente.edad = int(request.args["edad"]) if request.args.get("edad") else 0
    cliente.direccion = request.args.get("direccion", "")
    cliente.telefono = request.args.get("telefono", "")
    cliente.correo = request.args.get("correo", "")
    

    ClientesController.insertar(cliente)
    return "Cliente insertado exitosamente"

@app.route('/buscar_cliente')
def buscar_cliente():
    cliente_encontrado = ClientesController.buscar(request.args["cliente_buscado"])
    if cliente_encontrado:
        return f"Cliente encontrado: {cliente_encontrado.nombre}, Cédula: {cliente_encontrado.cedula}, Edad: {cliente_encontrado.edad}"
    else:
        return "Cliente no encontrado"

@app.route('/guardar_propiedad')
def guardar_propiedad():
    # Crear una propiedad
    codigo_str = request.args.get("codigo_propiedad", "").strip()
    codigo = int(codigo_str) if codigo_str else 0
    
    propiedad = Propiedad(codigo_propiedad=codigo, cedula_cliente="", valor_propiedad=0, direccion="", area=0, tipo="")
    propiedad.cedula_cliente = request.args["cedula_cliente"]
    propiedad.valor_propiedad = float(request.args.get("valor_propiedad", 0)) if request.args.get("valor_propiedad") else None
    propiedad.direccion = request.args.get("direccion", "")
    propiedad.area = float(request.args.get("area", 0)) if request.args.get("area") else None
    propiedad.tipo = request.args.get("tipo", "")

    if codigo == 0:
        conexion = PropiedadesController.conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            insert into propiedades (cedula_cliente, valor_propiedad, direccion, area, tipo)
            values (%s, %s, %s, %s, %s);
        """, (propiedad.cedula_cliente, propiedad.valor_propiedad, propiedad.direccion, 
              propiedad.area, propiedad.tipo))
        conexion.commit()
        conexion.close()
    else:
        PropiedadesController.insertar(propiedad)
    return "Propiedad insertada exitosamente"

@app.route('/buscar_propiedad')
def buscar_propiedad():
    propiedad_encontrada = PropiedadesController.buscar(int(request.args["propiedad_buscada"]))
    if propiedad_encontrada:
        return f"Propiedad encontrada: Código: {propiedad_encontrada[0]}, Valor: ${float(propiedad_encontrada[2]):,.2f}, Tipo: {propiedad_encontrada[5]}"
    else:
        return "Propiedad no encontrada"

@app.route('/guardar_hipoteca')
def guardar_hipoteca():
    # Crear una hipoteca
    hipoteca = Hipoteca(id_hipoteca=None, codigo_propiedad="", porcentaje_prestamo=0, tasa_interes=0,
                        plazo_anios=0, renta_mensual=0, deuda_final=0, fecha_inicio=None, fecha_fin=None, estado="ACTIVA")
    hipoteca.codigo_propiedad = request.args["codigo_propiedad"]
    hipoteca.porcentaje_prestamo = float(request.args.get("porcentaje_prestamo", 0)) if request.args.get("porcentaje_prestamo") else 0
    hipoteca.tasa_interes = float(request.args.get("tasa_interes", 0)) if request.args.get("tasa_interes") else 0
    hipoteca.plazo_anios = int(request.args.get("plazo_anios", 0)) if request.args.get("plazo_anios") else 0
    hipoteca.renta_mensual = float(request.args.get("renta_mensual", 0)) if request.args.get("renta_mensual") else None
    hipoteca.deuda_final = float(request.args.get("deuda_final", 0)) if request.args.get("deuda_final") else None
    hipoteca.fecha_inicio = request.args.get("fecha_inicio") or None
    hipoteca.fecha_fin = request.args.get("fecha_fin") or None
    hipoteca.estado = request.args.get("estado", "ACTIVA")
    
    # Guardarla en la BD
    HipotecasController.insertar(hipoteca)
    return "Hipoteca insertada exitosamente"

@app.route('/buscar_hipoteca')
def buscar_hipoteca():
    hipoteca_encontrada = HipotecasController.buscar(int(request.args["hipoteca_buscada"]))
    if hipoteca_encontrada:
        return f"Hipoteca encontrada: ID: {hipoteca_encontrada.id_hipoteca}, Estado: {hipoteca_encontrada.estado}, Renta Mensual: ${float(hipoteca_encontrada.renta_mensual or 0):,.2f}"
    else:
        return "Hipoteca no encontrada"

@app.route('/guardar_heredero')
def guardar_heredero():
    # Crear un heredero
    heredero = Heredero(id_heredero=None, cedula_cliente="", nombre="", relacion="", telefono="", correo="")
    heredero.cedula_cliente = request.args["cedula_cliente"]
    heredero.nombre = request.args["nombre"]
    heredero.relacion = request.args.get("relacion", "")
    heredero.telefono = request.args.get("telefono", "")
    heredero.correo = request.args.get("correo", "")
    
    # Guardarla en la BD
    HerederosController.insertar(heredero)
    return "Heredero insertado exitosamente"

@app.route('/buscar_heredero')
def buscar_heredero():
    heredero_encontrado = HerederosController.buscar(int(request.args["heredero_buscado"]))
    if heredero_encontrado:
        return f"Heredero encontrado: ID: {heredero_encontrado[0]}, Nombre: {heredero_encontrado[2]}, Relación: {heredero_encontrado[3]}"
    else:
        return "Heredero no encontrado"

@app.route('/crear_tablas')
def crear_tablas():
    ClientesController.crear_tabla()
    PropiedadesController.crear_tabla()
    HipotecasController.crear_tabla()
    HerederosController.crear_tabla()
    return "Tablas creadas exitosamente"

# Esta linea permite que nuestra aplicación se ejecute individualmente
if __name__=='__main__':
   app.run( debug=True)
