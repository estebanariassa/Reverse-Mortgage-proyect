
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

@app.route('/menu')
def menu():
    return (
        """
        <h2>Menú de navegación</h2>
        <ul>
            <li><a href="/buscar_datos">Buscar datos</a></li>
            <li><a href="/crear_tablas">Crear tablas de la BD</a></li>
        </ul>
        """
    )

@app.route('/buscar_datos')
def buscar_datos():
    return render_template("buscar_datos.html")

@app.route('/guardar_cliente')
def guardar_cliente():
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

@app.route('/modificar_cliente')
def modificar_cliente():
    cedula = request.args.get("cedula")
    if not cedula:
        return "Debe enviar la cédula del cliente a modificar", 400

    existente = ClientesController.buscar(cedula)
    if not existente:
        return "Cliente no encontrado", 404

    nombre = request.args.get("nombre", existente.nombre)
    edad = int(request.args.get("edad", existente.edad or 0))
    direccion = request.args.get("direccion", existente.direccion or "")
    telefono = request.args.get("telefono", existente.telefono or "")
    correo = request.args.get("correo", existente.correo or "")

    conexion = ClientesController.conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE clientess
        SET nombre=%s, edad=%s, direccion=%s, telefono=%s, correo=%s
        WHERE cedula=%s;
        """,
        (nombre, edad, direccion, telefono, correo, cedula)
    )
    conexion.commit()
    conexion.close()
    return "Cliente modificado exitosamente"

@app.route('/guardar_propiedad')
def guardar_propiedad():
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

@app.route('/modificar_propiedad')
def modificar_propiedad():
    codigo_str = request.args.get("codigo_propiedad", "").strip()
    if not codigo_str:
        return "Debe enviar el código de la propiedad a modificar", 400
    codigo = int(codigo_str)

    existente = PropiedadesController.buscar(codigo)
    if not existente:
        return "Propiedad no encontrada", 404

    cedula_cliente = request.args.get("cedula_cliente", existente[1])
    valor_propiedad = request.args.get("valor_propiedad")
    valor_propiedad = float(valor_propiedad) if valor_propiedad not in (None, "") else existente[2]
    direccion = request.args.get("direccion", existente[3])
    area_val = request.args.get("area")
    area = float(area_val) if area_val not in (None, "") else existente[4]
    tipo = request.args.get("tipo", existente[5])

    conexion = PropiedadesController.conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE propiedades
        SET cedula_cliente=%s, valor_propiedad=%s, direccion=%s, area=%s, tipo=%s
        WHERE codigo_propiedad=%s;
        """,
        (cedula_cliente, valor_propiedad, direccion, area, tipo, codigo)
    )
    conexion.commit()
    conexion.close()
    return "Propiedad modificada exitosamente"

@app.route('/guardar_hipoteca')
def guardar_hipoteca():
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
    
    HipotecasController.insertar(hipoteca)
    return "Hipoteca insertada exitosamente"

@app.route('/buscar_hipoteca')
def buscar_hipoteca():
    hipoteca_encontrada = HipotecasController.buscar(int(request.args["hipoteca_buscada"]))
    if hipoteca_encontrada:
        return f"Hipoteca encontrada: ID: {hipoteca_encontrada.id_hipoteca}, Estado: {hipoteca_encontrada.estado}, Renta Mensual: ${float(hipoteca_encontrada.renta_mensual or 0):,.2f}"
    else:
        return "Hipoteca no encontrada"

@app.route('/modificar_hipoteca')
def modificar_hipoteca():
    id_str = request.args.get("id_hipoteca", "").strip()
    if not id_str:
        return "Debe enviar el ID de la hipoteca a modificar", 400
    id_hipoteca = int(id_str)

    existente = HipotecasController.buscar(id_hipoteca)
    if not existente:
        return "Hipoteca no encontrada", 404

    codigo_propiedad = request.args.get("codigo_propiedad", existente.codigo_propiedad)
    porcentaje_prestamo = request.args.get("porcentaje_prestamo")
    porcentaje_prestamo = float(porcentaje_prestamo) if porcentaje_prestamo not in (None, "") else existente.porcentaje_prestamo
    tasa_interes = request.args.get("tasa_interes")
    tasa_interes = float(tasa_interes) if tasa_interes not in (None, "") else existente.tasa_interes
    plazo_anios = request.args.get("plazo_anios")
    plazo_anios = int(plazo_anios) if plazo_anios not in (None, "") else existente.plazo_anios
    renta_mensual = request.args.get("renta_mensual")
    renta_mensual = float(renta_mensual) if renta_mensual not in (None, "") else existente.renta_mensual
    deuda_final = request.args.get("deuda_final")
    deuda_final = float(deuda_final) if deuda_final not in (None, "") else existente.deuda_final
    fecha_inicio = request.args.get("fecha_inicio", existente.fecha_inicio)
    fecha_fin = request.args.get("fecha_fin", existente.fecha_fin)
    estado = request.args.get("estado", existente.estado)

    conexion = HipotecasController.conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE hipotecas
        SET codigo_propiedad=%s, porcentaje_prestamo=%s, tasa_interes=%s, plazo_anios=%s,
            renta_mensual=%s, deuda_final=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s
        WHERE id_hipoteca=%s;
        """,
        (
            codigo_propiedad, porcentaje_prestamo, tasa_interes, plazo_anios,
            renta_mensual, deuda_final, fecha_inicio, fecha_fin, estado, id_hipoteca
        )
    )
    conexion.commit()
    conexion.close()
    return "Hipoteca modificada exitosamente"

@app.route('/guardar_heredero')
def guardar_heredero():
    heredero = Heredero(id_heredero=None, cedula_cliente="", nombre="", relacion="", telefono="", correo="")
    heredero.cedula_cliente = request.args["cedula_cliente"]
    heredero.nombre = request.args["nombre"]
    heredero.relacion = request.args.get("relacion", "")
    heredero.telefono = request.args.get("telefono", "")
    heredero.correo = request.args.get("correo", "")
    
    HerederosController.insertar(heredero)
    return "Heredero insertado exitosamente"

@app.route('/buscar_heredero')
def buscar_heredero():
    heredero_encontrado = HerederosController.buscar(int(request.args["heredero_buscado"]))
    if heredero_encontrado:
        return f"Heredero encontrado: ID: {heredero_encontrado[0]}, Nombre: {heredero_encontrado[2]}, Relación: {heredero_encontrado[3]}"
    else:
        return "Heredero no encontrado"

@app.route('/modificar_heredero')
def modificar_heredero():
    id_str = request.args.get("id_heredero", "").strip()
    if not id_str:
        return "Debe enviar el ID del heredero a modificar", 400
    id_heredero = int(id_str)

    existente = HerederosController.buscar(id_heredero)
    if not existente:
        return "Heredero no encontrado", 404

    cedula_cliente = request.args.get("cedula_cliente", existente[1])
    nombre = request.args.get("nombre", existente[2])
    relacion = request.args.get("relacion", existente[3])
    telefono = request.args.get("telefono", existente[4])
    correo = request.args.get("correo", existente[5])

    conexion = HerederosController.conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE herederos
        SET cedula_cliente=%s, nombre=%s, relacion=%s, telefono=%s, correo=%s
        WHERE id_heredero=%s;
        """,
        (cedula_cliente, nombre, relacion, telefono, correo, id_heredero)
    )
    conexion.commit()
    conexion.close()
    return "Heredero modificado exitosamente"

@app.route('/crear_tablas')
def crear_tablas():
    ClientesController.crear_tabla()
    PropiedadesController.crear_tabla()
    HipotecasController.crear_tabla()
    HerederosController.crear_tabla()
    return "Tablas creadas exitosamente"

if __name__=='__main__':
   app.run( debug=True)
