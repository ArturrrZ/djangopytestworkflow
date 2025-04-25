import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_add_user_successful(api_client):
    response = api_client.post('/api/users/', {"username": "testuser", "password": "testpass123"})
    assert response.status_code == 201
    

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpass123"}

@pytest.mark.django_db
def test_create_user_success(api_client, user_data):
    response = api_client.post('/api/users/', user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'user_id' in response.data

@pytest.mark.django_db
def test_create_user_missing_fields(api_client):
    response = api_client.post('/api/users/', {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data

@pytest.mark.django_db
def test_create_user_already_exists(api_client, user_data):
    User.objects.create_user(**user_data)
    response = api_client.post('/api/users/', user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data

@pytest.mark.django_db
def test_get_users(api_client, user_data):
    User.objects.create_user(**user_data)
    response = api_client.get('/api/users/')
    assert response.status_code == status.HTTP_200_OK
    assert 'users' in response.data
    assert any(user["username"] == user_data["username"] for user in response.data["users"])

@pytest.fixture
def authenticated_client(api_client):
    user = User.objects.create_user(username="secureuser", password="securepass")
    api_client.login(username="secureuser", password="securepass")
    return api_client

@pytest.mark.django_db
def test_secured_view_authenticated(authenticated_client):
    response = authenticated_client.get('/api/secured/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "secured"

@pytest.mark.django_db
def test_secured_view_unauthenticated(api_client):
    response = api_client.get('/api/secured/')
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED, status.HTTP_302_FOUND]

    
