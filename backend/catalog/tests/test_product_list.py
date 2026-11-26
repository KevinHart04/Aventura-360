from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.test import Client

from catalog.models import Product

URL = "/api/products/"


def make_product(**overrides: object) -> Product:
    data: dict[str, object] = {
        "sku": "CAMP-001",
        "name": "Carpa Domo 4 personas",
        "brand": "Andes",
        "price": Decimal("129999.90"),
        "stock": 10,
        "image_url": "https://example.com/carpa.jpg",
    }
    data.update(overrides)
    return Product.objects.create(**data)


def results_by_sku(client: Client) -> dict[str, dict[str, object]]:
    response = client.get(URL)
    assert response.status_code == 200
    return {item["sku"]: item for item in response.json()["results"]}


@pytest.mark.django_db
def test_anonymous_visitor_can_list_products(client: Client) -> None:
    make_product()

    response = client.get(URL)

    assert response.status_code == 200
    assert response.json()["count"] == 1


@pytest.mark.django_db
def test_product_exposes_catalog_fields(client: Client) -> None:
    make_product()

    item = results_by_sku(client)["CAMP-001"]

    assert item == {
        "id": item["id"],
        "sku": "CAMP-001",
        "name": "Carpa Domo 4 personas",
        "brand": "Andes",
        "price": "129999.90",
        "image_url": "https://example.com/carpa.jpg",
        "stock": 10,
        "availability": "in_stock",
    }


@pytest.mark.django_db
def test_out_of_stock_product_is_still_listed(client: Client) -> None:
    make_product(sku="SIN-STOCK", stock=0)

    item = results_by_sku(client)["SIN-STOCK"]

    assert item["availability"] == "out_of_stock"


@pytest.mark.django_db
def test_product_with_one_unit_is_flagged_as_last_unit(client: Client) -> None:
    make_product(sku="ULTIMA", stock=1)
    make_product(sku="DOS", stock=2)

    items = results_by_sku(client)

    assert items["ULTIMA"]["availability"] == "last_unit"
    assert items["DOS"]["availability"] == "in_stock"


@pytest.mark.django_db
def test_inactive_products_are_not_listed(client: Client) -> None:
    make_product(sku="ACTIVO")
    make_product(sku="INACTIVO", is_active=False)

    items = results_by_sku(client)

    assert set(items) == {"ACTIVO"}


@pytest.mark.django_db
def test_price_keeps_exact_decimals(client: Client) -> None:
    make_product(price=Decimal("0.10"))

    item = results_by_sku(client)["CAMP-001"]

    assert item["price"] == "0.10"


@pytest.mark.django_db
def test_products_are_listed_in_stable_order(client: Client) -> None:
    make_product(sku="B", name="Mochila")
    make_product(sku="A", name="Bastón")

    response = client.get(URL)

    assert [item["name"] for item in response.json()["results"]] == ["Bastón", "Mochila"]


@pytest.mark.django_db
def test_list_is_paginated(client: Client) -> None:
    for number in range(25):
        make_product(sku=f"SKU-{number:02d}", name=f"Producto {number:02d}")

    first_page = client.get(URL).json()
    second_page = client.get(URL, {"page": 2}).json()

    assert first_page["count"] == 25
    assert len(first_page["results"]) == 20
    assert len(second_page["results"]) == 5


@pytest.mark.django_db
@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_catalog_is_read_only(client: Client, method: str) -> None:
    product = make_product()

    list_response = getattr(client, method)(URL, {}, content_type="application/json")
    detail_response = getattr(client, method)(
        f"{URL}{product.pk}/", {}, content_type="application/json"
    )

    assert list_response.status_code == 405
    assert detail_response.status_code == 404
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_negative_price_is_rejected_by_database() -> None:
    with pytest.raises(IntegrityError):
        make_product(price=Decimal("-1.00"))
