class Hipoteca:
    def __init__(self, id_hipoteca, codigo_propiedad, porcentaje_prestamo, tasa_interes,
                 plazo_anios, renta_mensual, deuda_final, fecha_inicio, fecha_fin, estado):
        self.id_hipoteca = id_hipoteca
        self.codigo_propiedad = codigo_propiedad
        self.porcentaje_prestamo = porcentaje_prestamo
        self.tasa_interes = tasa_interes
        self.plazo_anios = plazo_anios
        self.renta_mensual = renta_mensual
        self.deuda_final = deuda_final
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def __repr__(self):
        return f"Hipoteca({self.id_hipoteca}, Propiedad={self.codigo_propiedad}, Estado={self.estado})"
