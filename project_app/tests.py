import pytest
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
