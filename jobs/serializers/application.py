from rest_framework import serializers
from datetime import date
from jobs.models import JobApplication
from jobs import enums as job_status_enums


class JobApplicationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=job_status_enums.JobApplicationStatus.choices
    )
    applied_date = serializers.DateField()

    class Meta:
        model = JobApplication
        fields = ["id", "job_title", "company_name", "status", "applied_date", "notes"]

    def validate_applied_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Applied date cannot be in the future.")
        return value
