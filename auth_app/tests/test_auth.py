import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username='existing_user',
        email='existing@test.com',
        password='existing_password'
    )
    return user


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    response = client.post('/auth/register/', {
        'username': 'test_user',
        'email': 'test@test.com',
        'password': 'test_password'
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully'
    assert response.data['token'] is not None


@pytest.mark.django_db
def test_login_user(create_user):
    client = APIClient()
    response = client.post('/auth/login/', {
        'username': 'existing_user',
        'password': 'existing_password'
    })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_failed_login():
    client = APIClient()
    response = client.post('/auth/login/', {
        'username': 'non_existing_user',
        'password': 'non_existing_password'
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
