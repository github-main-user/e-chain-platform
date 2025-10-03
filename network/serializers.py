from rest_framework import serializers

from network.models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "created_at",
            "level",
            "products",
        ]
        read_only_fields = ("created_at", "level")

    def update(self, instance, validated_data):
        # изменение debt при update запрещено
        if "debt" in validated_data:
            validated_data.pop("debt")

        return super().update(instance, validated_data)
