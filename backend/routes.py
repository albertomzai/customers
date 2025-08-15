"""API endpoints for managing clientes."""

from flask import Blueprint, request, jsonify, abort
from .models import Cliente
from . import db

clientes_bp = Blueprint('clientes', __name__)

# Allowed status values
_ALLOWED_STATUS = {'Activo', 'Inactivo', 'Potencial'}

def _validate_cliente_data(data, require_all=True):
    """Validate incoming cliente data.

    Args:
        data (dict): Payload from request.json.
        require_all (bool): Whether all fields must be present.
    Returns:
        dict: Validated data.
    Raises:
        abort(400): If validation fails.
    """

    required_fields = {'nombre_completo', 'email', 'status'}
    if require_all and not required_fields.issubset(data.keys()):
        missing = required_fields - data.keys()
        abort(400, description=f'Missing fields: {missing}')

    # Validate status
    status = data.get('status')
    if status and status not in _ALLOWED_STATUS:
        abort(400, description='Invalid status value.')

    return data

@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    """Return a list of all clientes."""
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

@clientes_bp.route('/', methods=['POST'])
def create_cliente():
    """Create a new cliente."""
    data = request.get_json() or {}
    _validate_cliente_data(data)

    cliente = Cliente(**data)
    db.session.add(cliente)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    """Update an existing cliente."""
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.get_json() or {}
    _validate_cliente_data(data, require_all=False)

    for key, value in data.items():
        if hasattr(cliente, key):
            setattr(cliente, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=str(e))

    return jsonify(cliente.to_dict()), 200

@clientes_bp.route('/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    """Delete a cliente."""
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'message': 'Cliente deleted'}), 200