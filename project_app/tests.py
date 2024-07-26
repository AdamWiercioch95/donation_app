import pytest
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
