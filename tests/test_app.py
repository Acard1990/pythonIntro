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
    response = client.get('/appUsers')
    assert b'User CRUD App' in response.data

def test_add_user(setup):
    response = client.post('/appUsers', data={'first_name': 'John', 'last_name': 'Doe', 'email': 'johndoe@example.com'})

    # Validate a user exists
    added_user = User.query.filter_by(first_name='John', last_name='Doe').first()
    assert added_user is not None

    # Validate first name, last name, and email values
    assert added_user.first_name == 'John'
    assert added_user.last_name == 'Doe'
    assert added_user.email == 'johndoe@example.com'

    # Validate the response is a redirect
    assert response.status_code == 302

def test_update_user(setup):
    user = User(first_name='John', last_name='Doe', email='johndoe@example.com')
    setup.session.add(user)
    setup.session.commit()

    # Validate a user exists
    response = client.post('/appUsers/update/1', data={'first_name': 'Updated', 'last_name': 'User', 'email': 'updated@example.com'})
    updated_user = User.query.get(1)
    assert updated_user is not None

    # Validate first name, last name, and email values
    assert updated_user.first_name == 'Updated'
    assert updated_user.last_name == 'User'
    assert updated_user.email == 'updated@example.com'

    # Validate the response is a redirect
    assert response.status_code == 302

def test_delete_user(setup):
    user = User(first_name='John', last_name='Doe', email='johndoe@example.com')
    setup.session.add(user)
    setup.session.commit()

    # Validate user exists
    client.get('/appUsers/delete/1')
    assert User.query.get(1) is None

