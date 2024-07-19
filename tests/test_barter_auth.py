from rest_framework import status
import pytest
from barter_auth.models import BarterUser


#region Register tests
@pytest.mark.django_db
def test_valid_register(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': '',  # Empty referral code is valid
        'terms_and_conditions_accepted': True,
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert BarterUser.objects.filter(username='johndoe').exists()

@pytest.mark.django_db
def test_invalid_register_missing_fields(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {}  # Missing required fields

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_invalid_register_duplicate_email(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': '',
        'terms_and_conditions_accepted': True,
    }

    # Create a user with the same email
    BarterUser.objects.create_user(
        username='existinguser',
        email='johndoe@example.com',
        password='password'
    )

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_invalid_register_duplicate_username(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': '',
        'terms_and_conditions_accepted': True,
    }

    # Create a user with the same username
    BarterUser.objects.create_user(
        username='johndoe',
        email='anotheruser@example.com',
        password='password'
    )

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_valid_register_existing_referral_code(api_client):
    url = '/api/v2/barter_auth/register/'

    # Create a user with an existing referral code
    existing_user = BarterUser.objects.create_user(
        username='existinguser',
        email='existinguser@example.com',
        password='password',
        referral_code='existing-referral-code'
    )

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': 'existing-referral-code',  # Existing referral code
        'terms_and_conditions_accepted': True,
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert BarterUser.objects.filter(username='johndoe').exists()

    # Verify that the referred_by field is set correctly for the newly registered user
    new_user = BarterUser.objects.get(username='johndoe')
    assert new_user.referred_by == existing_user

@pytest.mark.django_db
def test_invalid_register_nonexistent_referral_code(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': 'nonexistent-referral-code',  # Nonexistent referral code
        'terms_and_conditions_accepted': True,
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.django_db
def test_register_missing_terms_and_conditions(api_client):
    url = '/api/v2/barter_auth/register/'

    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'phone_number': '1234567890',
        'country': 'USA',
        'city': 'New York',
        'address': '123 Street',
        'zip_code': '12345',
        'referral_code': '',
        'terms_and_conditions_accepted': False,
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
#endregion

#region Login tests
@pytest.mark.django_db
def test_correct_login(api_client):
    url = '/api/v2/barter_auth/login/'

    # Create a user for testing
    BarterUser.objects.create_user(
        username='johndoe',
        email='johndoe@example.com',
        password='password'
    )

    data = {
        'username': 'johndoe@example.com',
        'password': 'password',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data

@pytest.mark.django_db
def test_incorrect_login(api_client):
    url = '/api/v2/barter_auth/login/'

    # Create a user for testing
    BarterUser.objects.create_user(
        username='johndoe',
        email='johndoe@example.com',
        password='password'
    )

    data = {
        'username': 'johndoe@example.com',
        'password': 'wrong-password',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_login_inactive_user(api_client):
    url = '/api/v2/barter_auth/login/'

    # Create an inactive user for testing
    BarterUser.objects.create_user(
        username='inactiveuser',
        email='inactiveuser@example.com',
        password='password',
        is_active=False
    )

    data = {
        'username': 'inactiveuser',
        'password': 'password',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_login_nonexistent_user(api_client):
    url = '/api/v2/barter_auth/login/'

    data = {
        'username': 'nonexistentuser',
        'password': 'password',
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
#endregion
