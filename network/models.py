from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    supplier = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="clients"
    )
    level = models.PositiveSmallIntegerField(editable=False, default=0)
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["country"]),
        ]

    def __str__(self):
        return f"{self.name} (lvl {self.level})"

    def clean(self) -> None:
        level = 0
        seen = set()
        current = self.supplier

        while current is not None:
            if not current.pk:
                break  # current node is not saved yet, validate later

            if current.pk in seen:
                raise ValidationError("Cyclic dependence of suppliers is not allowed")

            seen.add(current.pk)

            level += 1
            if level > 2:
                raise ValidationError("Hierarchy can't be deeper than 2")

            current = current.supplier
        self.level = level

    def save(self, *args, **kwargs) -> None:
        self.clean()
        return super().save(*args, **kwargs)


class Product(models.Model):
    node = models.ForeignKey(
        NetworkNode, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        return f"{self.name} {self.model}"
