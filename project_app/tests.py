import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_landing_page_view(client):
    url = reverse('landing_page')
    response = client.get(url)
    assert response.status_code == 200
