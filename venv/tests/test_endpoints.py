import pytest
from app import app, db, DadosColetados


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://:memory:'

    with app.app_context():
        db.create_all()

    client = app.test_client()
    return client

def test_post_leak(client):

    response = client.post('/leak', json={
        "user": "test_user",
        "senha": "test123",
        "origem_ip": "127.0.0.1"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data['message'] == 'Dados coletados com sucesso'
    assert "id" in data

def test_get_dados(client):
    with app.app_context():
        db.session.add(DadosColetados(user="joao", senha="senha", origem_ip="1.2.3.4"))
        db.session.commit()

    response = client.get('/dados')
    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert any(d["user"] == "joao" and d["senha"] == "senha" for d in data)

def test_delete_dado(client):
    with app.app_context():
        dado = DadosColetados(user="temp", senha="123", origem_ip="1.1.1.1")
        db.session.add(dado)
        db.session.commit()
        id = dado.id

    response = client.delete(f'/apagar/{id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Dado apagado com sucesso"              
