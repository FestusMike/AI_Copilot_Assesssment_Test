import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from faker import Faker
from jobs import enums as job_status_enums

faker = Faker()


@pytest.mark.django_db
def test_create_job_application(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "job_title": faker.job(),
        "company_name": faker.company(),
        "status": job_status_enums.JobApplicationStatus.APPLIED,
        "applied_date": faker.date_this_decade().isoformat(),
        "notes": faker.sentence(),
    }
    print(data)
    response = api_client.post(reverse("job-application-list"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert response.data["message"] == "Job application created successfully."


@pytest.mark.django_db
def test_create_job_application_future_date(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "job_title": faker.job(),
        "company_name": faker.company(),
        "status": job_status_enums.JobApplicationStatus.APPLIED,
        "applied_date": "2099-12-31",
        "notes": faker.sentence(),
    }
    response = api_client.post(reverse("job-application-list"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Applied date cannot be in the future." in str(response.data)


@pytest.mark.django_db
def test_list_job_applications(api_client, user, job_application):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("job-application-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert len(response.data["data"]) > 0


@pytest.mark.django_db
def test_retrieve_job_application(api_client, user, job_application):
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse("job-application-detail", args=[job_application.id])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True


@pytest.mark.django_db
def test_update_job_application(api_client, user, job_application):
    api_client.force_authenticate(user=user)
    updated_data = {"status": "Interview Scheduled"}
    response = api_client.patch(
        reverse("job-application-detail", args=[job_application.id]), updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"]["status"] == "Interview Scheduled"


@pytest.mark.django_db
def test_delete_job_application(api_client, user, job_application):
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse("job-application-detail", args=[job_application.id])
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
