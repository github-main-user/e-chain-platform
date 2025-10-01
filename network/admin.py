from django.contrib import admin
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "node", "release_date")


@admin.action(description="Очистить задолженность у выбранных")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "country",
        "city",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country", "level")
    search_fields = ("name", "city", "country", "email")
    actions = [clear_debt]
    readonly_fields = ("level", "created_at", "supplier_link")

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/networknode/{}/change/">{}</a>',
                obj.supplier.pk,
                obj.supplier.name,
            )
        return "-"

    supplier_link.short_description = "Ссылка на поставщика"
