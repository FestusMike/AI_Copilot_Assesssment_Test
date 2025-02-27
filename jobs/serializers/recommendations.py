from rest_framework import serializers
from jobs.models import JobRecommendation


class JobRecommendationSerializer(serializers.ModelSerializer):
    job_url = serializers.URLField()

    class Meta:
        model = JobRecommendation
        fields = ["id", "job_title", "company_name", "job_url", "posted_at"]
