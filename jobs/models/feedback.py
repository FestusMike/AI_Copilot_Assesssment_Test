from django.db import models
from users.models import UserAccount
from includes.helpers import models as helper_models
from jobs import enums as job_status_enums


class ResumeFeedback(helper_models.PrimaryKeyMixin, helper_models.DateHistoryMixin):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="resume_feedbacks"
    )
    resume_text = models.TextField()
    feedback = models.JSONField(default=dict)

    def generate_mock_feedback(self):
        import random

        suggestions = [
            suggestion.value for suggestion in job_status_enums.MockFeedbackSuggestions
        ]
        self.feedback = {"suggestions": random.sample(suggestions, k=3)}
        self.save()

    def __str__(self):
        return f"Resume feedback for {self.user.first_name} {self.user.last_name}"
