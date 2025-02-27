from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as rest_auth
from jobs.models import JobRecommendation
from jobs.serializers import JobRecommendationSerializer
from includes.drf import APIResponseSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Job Recommendations",
        description="Fetch job recommendations based on the authenticated user's saved skills.",
        tags=["Job Recommendations"],
        responses={
            200: OpenApiResponse(
                response=JobRecommendationSerializer(many=True),
                description="Job recommendations fetched successfully.",
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    )
)
class JobRecommendationViewSet(viewsets.GenericViewSet):
    queryset = JobRecommendation.objects.all()
    serializer_class = JobRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [rest_auth.JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Job recommendations fetched successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )
