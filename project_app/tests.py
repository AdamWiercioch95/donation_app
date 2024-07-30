import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

from project_app.models import Donation


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


@pytest.mark.django_db
def test_add_donation_view_get(client, user):
    client.force_login(user)
    url = reverse('add_donation')
    response = client.get(url)

    assert response.status_code == 200
    assert 'categories' in response.context
    assert 'organizations' in response.context
    for organization in response.context['organizations']:
        assert hasattr(organization, 'category_ids_json')


@pytest.mark.django_db
def test_add_donation_view_post_success(client, user, category, institution):
    client.force_login(user)
    url = reverse('add_donation')
    data = {
        'bags': '3',
        'categories': [category.id],
        'organization': institution.id,
        'address': 'test address',
        'phone': '111222333',
        'city': 'test city',
        'postcode': '12-345',
        'data': '2024-10-01',
        'time': '10:00',
        'more_info': 'Careful',
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('confirm')
    assert Donation.objects.count() == 1
    donation = Donation.objects.first()
    assert donation.quantity == 3
    assert donation.address == 'test address'
    assert donation.phone_number == '111222333'
    assert donation.city == 'test city'
    assert donation.zip_code == '12-345'
    assert donation.pick_up_date.strftime('%Y-%m-%d') == '2024-10-01'
    assert donation.pick_up_time.strftime('%H:%M') == '10:00'
    assert donation.pick_up_comment == 'Careful'
    assert donation.institution == institution
    assert list(donation.categories.all()) == [category]


@pytest.mark.django_db
def test_add_donation_view_post_missing_fields(client, user):
    client.force_login(user)
    url = reverse('add_donation')
    data = {
        'bags': '',
        'categories': [],
        'organization': '',
        'address': '',
        'phone': '',
        'city': '',
        'postcode': '',
        'data': '',
        'time': '',
        'more_info': '',
    }
    response = client.post(url, data)

    assert response.status_code == 400
    assert 'Missing required fields.' in response.content.decode()


@pytest.mark.django_db
def test_add_donation_view_post_invalid_organization(client, user):
    client.force_login(user)
    url = reverse('add_donation')
    data = {
        'bags': '3',
        'categories': [1],
        'organization': 999,  # Invalid organization ID
        'address': '123 Main St',
        'phone': '555-555-5555',
        'city': 'Sample City',
        'postcode': '12345',
        'data': '2024-10-01',
        'time': '10:00',
        'more_info': 'Leave at the door',
    }
    response = client.post(url, data)

    assert response.status_code == 400
    assert 'Invalid organization.' in response.content.decode()


@pytest.mark.django_db
def test_confirm_donation_view_get_authenticated(client, user):
    client.force_login(user)
    url = reverse('confirm')
    response = client.get(url)

    assert response.status_code == 200
    assert 'form-confirmation.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_confirm_donation_view_get_unauthenticated(client):
    url = reverse('confirm')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')
    assert 'next=' in response.url
    assert response.url == f"/accounts/login/?next={url}"
