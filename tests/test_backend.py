# Test de la capa backend utilizando importación relativa

import os
import sys

# Si Pytest no encuentra el paquete, añadimos la ruta raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from ..backend import app as flask_app, db, Cliente

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    # Usar una base de datos temporal para cada test
    db_path = tmp_path / 'test.db'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    with flask_app.app_context():
        db.create_all()

    yield

    # Limpieza después del test
    with flask_app.app_context():
        db.drop_all()

def test_get_clientes_empty(client):
    response = client.get('/api/clientes')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_cliente(client):
    payload = {
        'nombre_completo': 'Juan Pérez',
        'empresa': 'Acme Corp',
        'email': 'juan@example.com',
        'telefono': '123456789',
        'status': 'Activo'
    }
    response = client.post('/api/clientes', json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data['nombre_completo'] == payload['nombre_completo']

def test_update_cliente(client):
    # Crear cliente primero
    client.post('/api/clientes', json={
        'nombre_completo': 'Ana',
        'email': 'ana@example.com',
        'status': 'Potencial'}),

    # Actualizar status
    response = client.put('/api/clientes/1', json={'status': 'Activo'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Activo'

def test_delete_cliente(client):
    # Crear cliente primero
    client.post('/api/clientes', json={
        'nombre_completo': 'Luis',
        'email': 'luis@example.com',
        'status': 'Inactivo'}),

    response = client.delete('/api/clientes/1')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Cliente eliminado'

    # Verificar que ya no existe
    get_resp = client.get('/api/clientes')
    assert get_resp.get_json() == []