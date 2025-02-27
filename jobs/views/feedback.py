from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from jobs.models import ResumeFeedback
from jobs.serializers import ResumeFeedbackSerializer
from jobs.permissions import IsOwner
from rest_framework_simplejwt import authentication as rest_auth
from includes.drf import APIResponseSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse


@extend_schema_view(
    create=extend_schema(
        summary="Create Resume Feedback",
        description="Submit a resume for AI-generated feedback. Only the authenticated user can create feedback.",
        request=ResumeFeedbackSerializer,
        responses={
            201: OpenApiResponse(
                response=ResumeFeedbackSerializer,
                description="Resume feedback created successfully.",
            ),
            400: OpenApiResponse(response=None, description="Invalid data provided."),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    list=extend_schema(
        summary="List Resume Feedback",
        description="Retrieve all resume feedback submitted by the authenticated user.",
        responses={
            200: OpenApiResponse(
                response=ResumeFeedbackSerializer(many=True),
                description="Resume feedback fetched successfully.",
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Resume Feedback",
        description="Fetch a specific resume feedback entry by ID. Only the owner can access their feedback.",
        responses={
            200: OpenApiResponse(
                response=ResumeFeedbackSerializer,
                description="Resume feedback fetched successfully.",
            ),
            404: OpenApiResponse(
                response=None, description="Resume feedback not found."
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete Resume Feedback",
        description="Delete a resume feedback entry. Only the owner can delete their own feedback.",
        responses={
            204: OpenApiResponse(
                response=APIResponseSerializer,
                description="Resume feedback deleted successfully.",
            ),
            404: OpenApiResponse(
                response=None, description="Resume feedback not found."
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
)
class ResumeFeedbackViewSet(viewsets.GenericViewSet):
    queryset = ResumeFeedback.objects.all()
    serializer_class = ResumeFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [rest_auth.JWTAuthentication]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        object = self.queryset.get(id=self.kwargs["pk"])
        self.check_object_permissions(self.request, object)
        return object

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Resume feedback created successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Resume feedback fetched successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        try:
            feedback = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Resume feedback not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(feedback)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Resume feedback fetched successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        try:
            feedback = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Resume feedback not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(feedback, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Resume feedback updated successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk=None):
        try:
            feedback = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Resume feedback not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(feedback, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Resume feedback updated successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        try:
            feedback = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Resume feedback not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        feedback.delete()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "success": True,
                    "message": "Resume feedback deleted successfully.",
                    "data": None,
                }
            ).data,
            status=status.HTTP_204_NO_CONTENT,
        )
