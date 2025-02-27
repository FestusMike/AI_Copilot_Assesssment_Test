import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_list_job_recommendations(api_client, user, job_recommendation):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("job-recommendation-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert len(response.data["data"]) > 0
