import pytest
from rest_framework import status

from faker import Faker
from rest_framework.reverse import reverse

fake = Faker()


@pytest.mark.django_db
def test_user_login(api_client, user, login_data):
    user.set_password(login_data["password"])
    user.save()
    response = api_client.post(reverse("user-authentication-user-login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data["data"]
    assert "refresh" in response.data["data"]


@pytest.mark.django_db
def test_user_login_invalid_password(api_client, user):
    data = {"email": user.email, "password": fake.password()}
    response = api_client.post(reverse("user-authentication-user-login"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid password" in response.data["errors"][0]["message"]


@pytest.mark.django_db
def test_user_login_invalid_email(api_client):
    data = {"email": fake.email(), "password": "password123"}
    response = api_client.post(reverse("user-authentication-user-login"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid email" in response.data["errors"][0]["message"]


@pytest.mark.django_db
def test_user_logout(api_client, user, refresh_token):
    response = api_client.post(
        reverse("user-authentication-user-logout"), {"refresh": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "User logged out successfully"


@pytest.mark.django_db
def test_user_logout_invalid_token(api_client):
    response = api_client.post(
        reverse("user-authentication-user-logout"), {"refresh": fake.uuid4()}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Logout Unsuccessful" in response.data["errors"][0]["message"]
