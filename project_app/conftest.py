import pytest

from django.contrib.auth.models import User
from django.test import Client

from .models import Donation, Institution, Category


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password', email='testuser@op.pl')


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', type=1)


@pytest.fixture
def institution(category):
    return Institution.objects.create(
        name='Test Institution',
        description='Test Institution',
        type=1,
        categories=category,
    )


@pytest.fixture
def donation(category, institution, user):
    return Donation.objects.create(
        quantity=5,
        categories=category,
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
