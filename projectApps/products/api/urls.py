from django.urls import path
from projectApps.products.api.views import (
    CategoryList,
    CategoryDetail,
    TypeAttributeList,
    TypeAttributeDetail,
    AttributeDefinitionList,
    AttributeDefinitionDetail,
    AttributeValueList,
    AttributeValueDetail,
    ProductList,
    ProductDetail,
)

app_name = "ProductApis"

urlpatterns = [
    # Category URLs
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    # TypeAttribute URLs
    path("type-attributes/", TypeAttributeList.as_view(), name="type-attribute-list"),
    path(
        "type-attributes/<int:pk>/",
        TypeAttributeDetail.as_view(),
        name="type-attribute-detail",
    ),
    # AttributeDefinition URLs
    path(
        "attribute-definitions/",
        AttributeDefinitionList.as_view(),
        name="attribute-definition-list",
    ),
    path(
        "attribute-definitions/<int:pk>/",
        AttributeDefinitionDetail.as_view(),
        name="attribute-definition-detail",
    ),
    # AttributeValue URLs
    path(
        "attribute-values/", AttributeValueList.as_view(), name="attribute-value-list"
    ),
    path(
        "attribute-values/<int:pk>/",
        AttributeValueDetail.as_view(),
        name="attribute-value-detail",
    ),
    # Product URLs
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
]
