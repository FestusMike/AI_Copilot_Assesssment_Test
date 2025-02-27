import pytest
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from users.models import UserAccount
from tests.factories import UserAccountFactory

fake = Faker()


@pytest.mark.django_db
def test_successful_registration(api_client):
    url = reverse("user-account-setup-user-registration")
    password = fake.password(
        length=12, special_chars=True, digits=True, upper_case=True
    )
    data = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": password,
        "password2": password,
        "skills": [fake.word() for _ in range(3)],
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert UserAccount.objects.filter(email=data["email"]).exists()


@pytest.mark.django_db
def test_registration_fails_when_passwords_do_not_match(api_client):
    url = reverse("user-account-setup-user-registration")
    data = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password(length=12),
        "password2": fake.password(length=12),
        "skills": [fake.word()],
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Passwords do not match" in response.data["errors"][0]["message"]


@pytest.mark.django_db
def test_registration_fails_when_email_already_exists(api_client):
    existing_user = UserAccountFactory(email=fake.email())
    url = reverse("user-account-setup-user-registration")
    password = fake.password(
        length=12, special_chars=True, digits=True, upper_case=True
    )
    data = {
        "email": existing_user.email,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": password,
        "password2": password,
        "skills": [fake.word()],
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This email already exists" in response.data["errors"][0]["message"]


@pytest.mark.django_db
def test_registration_fails_with_invalid_first_name(api_client):
    url = reverse("user-account-setup-user-registration")
    data = {
        "email": fake.email(),
        "first_name": "J0hn!",
        "last_name": fake.last_name(),
        "password": fake.password(length=12),
        "password2": fake.password(length=12),
        "skills": [fake.word()],
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid first name." in response.data["errors"][0]["message"]
