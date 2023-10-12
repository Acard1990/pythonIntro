import os
import pytest
from app import app, db, User

# Set the environment to 'testing' to use a separate database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
app.config['TESTING'] = True
client = app.test_client()

@pytest.fixture
def setup():
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

def test_index(setup):
    response = client.get('/')
    assert b'User CRUD App' in response.data

def test_add_user(setup):
    response = client.post('/add_user', data={'username': 'testuser', 'email': 'testuser@example.com'})

    # Validate a user exist
    added_user = User.query.filter_by(username='testuser').first()
    assert added_user is not None

    # Validate username and email values
    assert added_user.username == 'testuser'
    assert added_user.email == 'testuser@example.com'

    # Validate the response is a redirect
    assert response.status_code == 302

def test_update_user(setup):
    user = User(username='testuser', email='testuser@example.com')
    setup.session.add(user)
    setup.session.commit()

    # Validate a user exist
    response = client.post('/update_user/1', data={'username': 'updateduser', 'email': 'updated@example.com'})
    assert User.query.filter_by(username='updateduser').first() is not None

    # Validate username and email values
    assert user.username == 'updateduser'
    assert user.email == 'updated@example.com'

    # Validate the response is a redirect
    assert response.status_code == 302

def test_delete_user(setup):
    user = User(username='testuser', email='testuser@example.com')
    setup.session.add(user)
    setup.session.commit()

    # Validate no user found 
    client.get('/delete_user/1')
    assert User.query.get(1) is None
