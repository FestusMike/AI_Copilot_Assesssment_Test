from django.db import models
from includes.helpers import models as helper_models
from jobs import enums as job_status_enums
from users.models import UserAccount


class JobApplication(helper_models.DateHistoryMixin, helper_models.PrimaryKeyMixin):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="job_applications"
    )
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=job_status_enums.JobApplicationStatus.choices,
        default=job_status_enums.JobApplicationStatus.APPLIED,
    )
    applied_date = models.DateField()
    notes = models.TextField(blank=True)

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.job_title} at {self.company_name} - {self.status}"
