import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from faker import Faker

faker = Faker()


@pytest.mark.django_db
def test_create_resume_feedback(api_client, user):
    api_client.force_authenticate(user=user)
    data = {"resume_text": faker.text(max_nb_chars=200)}
    response = api_client.post(reverse("resume-feedback-list"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert response.data["message"] == "Resume feedback created successfully."


@pytest.mark.django_db
def test_create_resume_feedback_short_text(api_client, user):
    api_client.force_authenticate(user=user)
    data = {"resume_text": "Short text"}
    response = api_client.post(reverse("resume-feedback-list"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Resume text must be at least 50 characters long." in str(response.data)


@pytest.mark.django_db
def test_list_resume_feedbacks(api_client, user, resume_feedback):
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse("resume-feedback-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert len(response.data["data"]) > 0


@pytest.mark.django_db
def test_retrieve_resume_feedback(api_client, user, resume_feedback):
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse("resume-feedback-detail", args=[resume_feedback.id])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True


@pytest.mark.django_db
def test_update_resume_feedback(api_client, user, resume_feedback):
    api_client.force_authenticate(user=user)
    updated_data = {"resume_text": faker.text(max_nb_chars=200)}
    response = api_client.patch(
        reverse("resume-feedback-detail", args=[resume_feedback.id]), updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True


@pytest.mark.django_db
def test_delete_resume_feedback(api_client, user, resume_feedback):
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse("resume-feedback-detail", args=[resume_feedback.id])
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
