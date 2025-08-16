from flask import Blueprint, request, jsonify, abort
from .models import Cliente
from . import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Devuelve la lista de todos los clientes."""
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json() or {}
    required_fields = ['nombre_completo', 'email', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos requeridos faltantes'}), 400

    cliente = Cliente(**data)
    db.session.add(cliente)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(cliente, key) and key != 'id':
            setattr(cliente, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify(cliente.to_dict()), 200

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'}), 200