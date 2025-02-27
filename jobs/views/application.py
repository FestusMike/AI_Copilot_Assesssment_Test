from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as rest_auth
from jobs.models import JobApplication
from jobs.serializers import JobApplicationSerializer
from jobs.permissions import IsOwner
from includes.drf import APIResponseSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse


@extend_schema_view(
    list=extend_schema(
        summary="List Job Applications",
        description="Retrieve all job applications submitted by the authenticated user.",
        responses={
            200: OpenApiResponse(
                response=JobApplicationSerializer(many=True),
                description="Job applications fetched successfully.",
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Job Application",
        description="Fetch a specific job application by ID. Only the owner can access their application.",
        responses={
            200: OpenApiResponse(
                response=JobApplicationSerializer,
                description="Job application fetched successfully.",
            ),
            404: OpenApiResponse(
                response=None, description="Job application not found."
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    create=extend_schema(
        summary="Create Job Application",
        description="Submit a job application. Only the authenticated user can apply.",
        request=JobApplicationSerializer,
        responses={
            201: OpenApiResponse(
                response=JobApplicationSerializer,
                description="Job application created successfully.",
            ),
            400: OpenApiResponse(response=None, description="Invalid data provided."),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    update=extend_schema(
        summary="Update Job Application",
        description="Update an existing job application. Only the owner can update their application.",
        request=JobApplicationSerializer,
        responses={
            200: OpenApiResponse(
                response=JobApplicationSerializer,
                description="Job application updated successfully.",
            ),
            400: OpenApiResponse(response=None, description="Invalid data provided."),
            404: OpenApiResponse(
                response=None, description="Job application not found."
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete Job Application",
        description="Delete a job application. Only the owner can delete their application.",
        responses={
            204: OpenApiResponse(
                response=None, description="Job application deleted successfully."
            ),
            404: OpenApiResponse(
                response=None, description="Job application not found."
            ),
            401: OpenApiResponse(
                response=None,
                description="Authentication credentials were not provided or invalid.",
            ),
        },
    ),
)
class JobApplicationViewSet(viewsets.GenericViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
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
                    "message": "Job application created successfully.",
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
                    "message": "Job applications fetched successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        try:
            job_application = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Job application not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(job_application)
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Job application fetched successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        try:
            job_application = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Job application not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(job_application, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Job application updated successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk=None):
        try:
            job_application = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Job application not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(
            job_application, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Job application updated successfully.",
                    "data": serializer.data,
                }
            ).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        try:
            job_application = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                APIResponseSerializer(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "Job application not found.",
                        "data": None,
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        job_application.delete()
        return Response(
            APIResponseSerializer(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "success": True,
                    "message": "Job application deleted successfully.",
                    "data": None,
                }
            ).data,
            status=status.HTTP_204_NO_CONTENT,
        )
