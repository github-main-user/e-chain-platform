from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from .models import NetworkNode
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


@extend_schema_view(
    list=extend_schema(summary="List network nodes"),
    retrieve=extend_schema(summary="Retrieve a network node"),
    create=extend_schema(summary="Create a network node"),
    update=extend_schema(summary="Update a network node"),
    partial_update=extend_schema(summary="Update a network node partially"),
    destroy=extend_schema(summary="Delete a network node"),
)
class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related("supplier")
    serializer_class = NetworkNodeSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country"]
    search_fields = ["name", "city", "country"]
    ordering_fields = ["created_at", "name"]
    permission_classes = [IsActiveStaff]
