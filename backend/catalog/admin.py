from typing import TYPE_CHECKING

from django.contrib import admin

from .models import Product

# ModelAdmin es genérico solo en los stubs de tipos; en ejecución no se puede parametrizar.
if TYPE_CHECKING:
    ProductModelAdmin = admin.ModelAdmin[Product]
else:
    ProductModelAdmin = admin.ModelAdmin


@admin.register(Product)
class ProductAdmin(ProductModelAdmin):
    list_display = ("sku", "name", "brand", "price", "stock", "is_active")
    list_filter = ("is_active", "brand")
    search_fields = ("sku", "name", "brand")
