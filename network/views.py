from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import NetworkNode
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


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
