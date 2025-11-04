# Importamos Flask y los módulos necesarios
from flask import Flask, render_template, request

# Creamos la aplicación Flask
app = Flask(__name__)

# Ruta principal: muestra directamente el formulario hipotecas.html
@app.route('/')
def inicio():
    return render_template('hipotecas.html')

@app.route('/')
def inicio():
    return render_template('hipotecas.html')

# Ruta para procesar el formulario y calcular la hipoteca
@app.route('/calcular_hipoteca')
def calcular_hipoteca():
    valor_vivienda = float(request.args.get("valor_vivienda", 0))
    edad = int(request.args.get("edad", 0))
    porcentaje = float(request.args.get("porcentaje", 0))
    tasa = float(request.args.get("tasa", 0))

    # Cálculo básico (puedes ajustarlo según tus modelos)
    monto_prestamo = valor_vivienda * (porcentaje / 100)
    interes_mensual = tasa / 100 / 12
    cuotas = max(120 - (edad - 60) * 2, 12)  # estimado: menos edad = más cuotas
    cuota = monto_prestamo * interes_mensual / (1 - (1 + interes_mensual) ** -cuotas)

    return f"""
    <body style="background-color:#f5f5f5; color:black; font-family: Arial, sans-serif; padding: 20px;">
        <h2>Resultado del Cálculo</h2>
        <p>Valor de la vivienda: ${valor_vivienda:,.2f}</p>
        <p>Edad del propietario: {edad} años</p>
        <p>Monto del préstamo: ${monto_prestamo:,.2f}</p>
        <p>Cuotas estimadas: {cuotas}</p>
        <p>Cuota mensual: <b>${cuota:,.2f}</b></p>
        <a href="/">Volver</a>
    </body>
    """

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
