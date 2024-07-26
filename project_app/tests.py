import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_landing_page_view(client, donation):
    url = reverse('landing_page')
    response = client.get(url)
    assert response.status_code == 200
    assert 'total_bags' in response.context
    assert response.context['total_bags'] == 5
    assert 'institutions' in response.context
    assert len(response.context['institutions']) == 1
    assert 'institution_types' in response.context


@pytest.mark.django_db
def test_register_view_success(client):
    url = reverse('register')
    data = {
        'name': 'test_name',
        'surname': 'test_surname',
        'email': 'test@example.com',
        'password': 'password123',
        'password2': 'password123',
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('login')
    assert User.objects.filter(email='test@example.com').exists()


@pytest.mark.django_db
def test_register_view_password_mismatch(client):
    url = reverse('register')
    data = {
        'name': 'test_name',
        'surname': 'test_surname',
        'email': 'test@example.com',
        'password': 'password123',
        'password2': 'different_password123',
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'Podane hasła nie są takie same.' in response.content.decode()


@pytest.mark.django_db
def test_register_view_existing_user(client, user):
    url = reverse('register')
    data = {
        'name': user.first_name,
        'surname': user.last_name,
        'email': user.email,
        'password': user.password,
        'password2': user.password,
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'Użytkownik o podanym adresie email już istnieje.' in response.content.decode()
    assert User.objects.filter(email='testuser@op.pl').count() == 1


@pytest.mark.django_db
def test_login_view_success(client, user):
    url = reverse('login')
    data = {
        'email': 'testuser@op.pl',
        'password': 'password'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('landing_page')


@pytest.mark.django_db
def test_login_view_invalid_password(client, user):
    url = reverse('login')
    data = {
        'email': 'testuser@op.pl',
        'password': 'wrong_password'
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'Nieprawidłowe hasło.' in response.content.decode()
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_login_view_nonexistent_user(client):
    url = reverse('login')
    data = {
        'email': 'nonexistent@user.com',
        'password': 'password'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('register')
    assert not User.objects.filter(email='nonexistent@user.com').exists()


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username='testuser@op.pl', password='password')

    user = get_user_model().objects.get(username='testuser@op.pl')
    assert user.is_authenticated

    url = reverse('logout')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('landing_page')

    response = client.get(reverse('landing_page'))
    assert not response.wsgi_request.user.is_authenticated
