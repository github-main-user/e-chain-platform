from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import NetworkConfig
from .views import NetworkNodeViewSet

app_name = NetworkConfig.name


router = DefaultRouter()
router.register("nodes", NetworkNodeViewSet, "node")

urlpatterns = [
    path("", include(router.urls)),
]
