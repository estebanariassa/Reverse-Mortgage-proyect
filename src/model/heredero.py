class Heredero:
    """
    Clase que representa un heredero asociado a un cliente en el sistema de hipoteca inversa.
    """

    def __init__(self, id_heredero, cedula_cliente, nombre, relacion, telefono, correo):
        self.id_heredero = id_heredero                # Identificador único del heredero
        self.cedula_cliente = cedula_cliente          # Cédula del cliente al que pertenece
        self.nombre = nombre                          # Nombre completo del heredero
        self.relacion = relacion                      # Parentesco con el cliente
        self.telefono = telefono                      # Teléfono de contacto
        self.correo = correo                          # Correo electrónico del heredero

    def __str__(self):
        """
        Retorna una representación legible del heredero.
        """
        return (f"Heredero[{self.id_heredero}] - "
                f"Cliente: {self.cedula_cliente}, "
                f"Nombre: {self.nombre}, "
                f"Relación: {self.relacion}, "
                f"Teléfono: {self.telefono}")

    def to_tuple(self):
        """
        Devuelve los atributos como tupla para usar en operaciones SQL.
        """
        return (self.id_heredero, self.cedula_cliente, self.nombre,
                self.relacion, self.telefono, self.correo)
