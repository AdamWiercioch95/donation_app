import pytest

from django.contrib.auth.models import User
from django.test import Client

from .models import Donation, Institution, Category


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(
        first_name='test_name',
        last_name='test_lastname',
        username='testuser@op.pl',
        password='password',
        email='testuser@op.pl')


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')


@pytest.fixture
def institution(category):
    institution = Institution.objects.create(
        name='Test Institution',
        description='Test Institution',
        type=1,
    )
    institution.categories.add(category)
    return institution


@pytest.fixture
def donation(category, institution, user):
    donation = Donation.objects.create(
        quantity=5,
        institution=institution,
        address='test_address',
        phone_number='111222333',
        city='test_city',
        zip_code='11-111',
        pick_up_date='2024-10-01',
        pick_up_time='12:00:00',
        pick_up_comment='test comment',
        user=user,
        is_taken=False
    )
    donation.categories.add(category)
    return donation
