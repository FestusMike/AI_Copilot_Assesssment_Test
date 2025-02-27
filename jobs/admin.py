from django.contrib import admin
from jobs.models import ResumeFeedback, JobApplication, JobRecommendation

admin.site.register(ResumeFeedback)
admin.site.register(JobApplication)
admin.site.register(JobRecommendation)
