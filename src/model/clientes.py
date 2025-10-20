class Cliente:
    """Clase que representa un cliente en el sistema"""

    def __init__(self, cedula, nombre, edad, direccion=None, telefono=None, correo=None, fecha_registro=None):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_registro = fecha_registro

    def __repr__(self):
        return f"<Cliente {self.cedula} - {self.nombre}, {self.edad} años>"

    def to_dict(self):
        """Convierte el objeto en un diccionario"""
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "edad": self.edad,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "correo": self.correo,
            "fecha_registro": self.fecha_registro
        }

    @staticmethod
    def from_row(row):
        """Crea un objeto Cliente a partir de una fila de base de datos"""
        return Cliente(
            cedula=row[0],
            nombre=row[1],
            edad=row[2],
            direccion=row[3],
            telefono=row[4],
            correo=row[5],
            fecha_registro=row[6] if len(row) > 6 else None
        )
