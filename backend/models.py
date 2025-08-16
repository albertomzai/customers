from . import db

class Cliente(db.Model):
    """Modelo de cliente."""

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(120), nullable=False)
    empresa = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        """Serializa el cliente a un diccionario."""
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'empresa': self.empresa,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'status': self.status
        }