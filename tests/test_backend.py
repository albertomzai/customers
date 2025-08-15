import pytest

from backend import app, db, Cliente

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Create a clean database for each test
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
    # Teardown: drop tables again
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client():
    return app.test_client()

def test_get_empty(client):
    resp = client.get('/api/clientes/')
    assert resp.status_code == 200
    assert resp.json == []

def test_create_cliente(client):
    payload = {
        'nombre_completo': 'Juan Pérez',
        'empresa': 'Acme Corp',
        'email': 'juan@example.com',
        'telefono': '123456789',
        'status': 'Activo'
    }
    resp = client.post('/api/clientes/', json=payload)
    assert resp.status_code == 201
    data = resp.json
    assert data['nombre_completo'] == payload['nombre_completo']

def test_get_after_create(client):
    # Create first
    client.post('/api/clientes/', json={
        'nombre_completo': 'Ana',
        'empresa': 'Beta',
        'email': 'ana@example.com',
        'telefono': '',
        'status': 'Potencial'
    })
    resp = client.get('/api/clientes/')
    assert resp.status_code == 200
    assert len(resp.json) == 1

def test_update_cliente(client):
    # Create
    create_resp = client.post('/api/clientes/', json={
        'nombre_completo': 'Luis',
        'empresa': 'Gamma',
        'email': 'luis@example.com',
        'telefono': '',
        'status': 'Activo'
    })
    cid = create_resp.json['id']

    # Update
    update_payload = {'empresa': 'Delta', 'status': 'Inactivo'}
    resp = client.put(f'/api/clientes/{cid}', json=update_payload)
    assert resp.status_code == 200
    updated = resp.json
    assert updated['empresa'] == 'Delta'
    assert updated['status'] == 'Inactivo'

def test_delete_cliente(client):
    # Create
    create_resp = client.post('/api/clientes/', json={
        'nombre_completo': 'Carlos',
        'empresa': 'Epsilon',
        'email': 'carlos@example.com',
        'telefono': '',
        'status': 'Activo'
    })
    cid = create_resp.json['id']

    # Delete
    resp = client.delete(f'/api/clientes/{cid}')
    assert resp.status_code == 200
    assert resp.json['message'] == 'Cliente deleted'

    # Verify deletion
    get_resp = client.get('/api/clientes/')
    assert get_resp.json == []