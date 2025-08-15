"""Database models for the CRM backend."""

from . import db

class Cliente(db.Model):
    """Represents a customer record."""

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.Enum('Activo', 'Inactivo', 'Potencial', name='status_enum'), nullable=False)

    def to_dict(self):
        """Return a serializable representation of the client."""
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'empresa': self.empresa,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'status': self.status,
        }