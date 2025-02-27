from django.db import models
from users.models import UserAccount
from includes.helpers import models as helper_models


class JobRecommendation(helper_models.PrimaryKeyMixin, helper_models.DateHistoryMixin):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="job_recommendations"
    )
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_url = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
