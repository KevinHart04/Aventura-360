from rest_framework import serializers

from .models import Product


class ProductListSerializer(serializers.ModelSerializer[Product]):
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "sku", "name", "brand", "price", "image_url", "stock", "availability")
        read_only_fields = fields

    def get_availability(self, product: Product) -> str:
        if product.stock == 0:
            return "out_of_stock"
        if product.stock == 1:
            return "last_unit"
        return "in_stock"
