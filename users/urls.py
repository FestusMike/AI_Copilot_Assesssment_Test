from django.urls import path, include
from rest_framework import routers
from users.views import UserAccountViewSet, UserAuthViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter(trailing_slash=False)
router.register("", UserAccountViewSet, basename="user-account-setup")

auth_router = routers.DefaultRouter(trailing_slash=False)
auth_router.register("", UserAuthViewSet, basename="user-authentication")


urlpatterns = [
    path("accounts/", include(router.urls)),
    path("auth/", include(auth_router.urls)),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
