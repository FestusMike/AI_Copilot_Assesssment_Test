from django.db import models as dj_models
from enum import Enum


class JobApplicationStatus(dj_models.TextChoices):
    APPLIED = "Applied"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    OFFER_RECEIVED = "Offer Received"
    REJECTED = "Rejected"


class MockFeedbackSuggestions(Enum):
    ADD_MORE_ACTION_VERBS = "Add more action verbs."
    INCLUDE_MEASURABLE_ACHIEVEMENTS = "Include measurable achievements."
    OPTIMIZE_FOR_APPLICANT_TRACKING_SYSTEMS_ATS = (
        "Optimize for Applicant Tracking Systems (ATS)."
    )
    SHORTEN_YOUR_SUMMARY = "Shorten your summary."
    USE_A_PROFESSIONAL_EMAIL_ADDRESS = "Use a professional email address."

    def __str__(self):
        return self.value
