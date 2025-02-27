import pytest
from tests.factories import (
    UserAccountFactory,
    JobApplicationFactory,
    ResumeFeedbackFactory,
    JobRecommendationFactory,
)


@pytest.fixture
def user():
    return UserAccountFactory()


@pytest.fixture
def job_application(user):
    return JobApplicationFactory(user=user)


@pytest.fixture
def resume_feedback(user):
    return ResumeFeedbackFactory(user=user)


@pytest.fixture
def job_recommendation(user):
    return JobRecommendationFactory(user=user)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def login_data(user):
    return {"email": user.email, "password": "password123"}


@pytest.fixture
def refresh_token(user):
    from rest_framework_simplejwt.tokens import RefreshToken

    return str(RefreshToken.for_user(user))
