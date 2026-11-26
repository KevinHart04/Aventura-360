from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductListSerializer


class CatalogPagination(PageNumberPagination):
    page_size = 20


class ProductListView(ListAPIView[Product]):
    """Catálogo público: cualquier visitante puede verlo sin iniciar sesión (HU-04)."""

    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer
    pagination_class = CatalogPagination

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True)
