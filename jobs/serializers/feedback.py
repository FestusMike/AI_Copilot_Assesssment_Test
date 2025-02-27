from rest_framework import serializers
from jobs.models import ResumeFeedback


class ResumeFeedbackSerializer(serializers.ModelSerializer):
    resume_text = serializers.CharField()

    class Meta:
        model = ResumeFeedback
        fields = ["id", "resume_text", "feedback"]
        extra_kwargs = {
            "resume_text": {"required": True},
            "feedback": {"read_only": True},
        }

    def validate_resume_text(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError(
                "Resume text must be at least 50 characters long."
            )
        return value

    def create(self, validated_data):
        feedback_instance = ResumeFeedback.objects.create(**validated_data)
        feedback_instance.generate_mock_feedback()
        return feedback_instance
