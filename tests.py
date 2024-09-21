import pytest
from app import app, db, Message

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_message(client):
    response = client.post('/create', json={
        "account_id": "12345",
        "sender_number": "1234567890",
        "receiver_number": "0987654321"
    })
    assert response.status_code == 201

def test_get_messages(client):
    client.post('/create', json={
        "account_id": "12345",
        "sender_number": "1234567890",
        "receiver_number": "0987654321"
    })
    response = client.get('/get/messages/12345')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_search_messages(client):
    client.post('/create', json={
        "account_id": "12345",
        "sender_number": "1234567890",
        "receiver_number": "0987654321"
    })
    response = client.get('/search?sender_number=1234567890')
    assert response.status_code == 200
    assert len(response.get_json()) == 1

