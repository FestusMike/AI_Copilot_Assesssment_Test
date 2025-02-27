from django.urls import path, include
from rest_framework import routers
from jobs.views import (
    JobApplicationViewSet,
    JobRecommendationViewSet,
    ResumeFeedbackViewSet,
)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"job-applications", JobApplicationViewSet, basename="job-application")
router.register(
    r"job-recommendations", JobRecommendationViewSet, basename="job-recommendation"
)
router.register(r"resume-feedback", ResumeFeedbackViewSet, basename="resume-feedback")

urlpatterns = [
    path("", include(router.urls)),
]
