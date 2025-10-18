class Propiedad:
    """
    Clase que representa una propiedad dentro del sistema de hipoteca inversa.
    Cada propiedad está asociada a un cliente (cedula_cliente).
    """

    def __init__(self, codigo_propiedad, cedula_cliente, valor_propiedad, direccion, area, tipo):
        self.codigo_propiedad = codigo_propiedad          # Código único de la propiedad
        self.cedula_cliente = cedula_cliente              # Cédula del propietario
        self.valor_propiedad = valor_propiedad            # Valor de la vivienda (COP)
        self.direccion = direccion                        # Dirección completa
        self.area = area                                  # Área en metros cuadrados
        self.tipo = tipo                                  # Tipo de propiedad (Casa, Apartamento, Finca, etc.)

    def __str__(self):
        """
        Retorna una representación en texto de la propiedad.
        """
        return (f"Propiedad[{self.codigo_propiedad}] - "
                f"Cliente: {self.cedula_cliente}, "
                f"Valor: ${self.valor_propiedad:,.2f}, "
                f"Área: {self.area} m², "
                f"Tipo: {self.tipo}")

    def to_tuple(self):
        """
        Devuelve los atributos en forma de tupla para usar en consultas SQL.
        """
        return (self.codigo_propiedad, self.cedula_cliente, self.valor_propiedad,
                self.direccion, self.area, self.tipo)
