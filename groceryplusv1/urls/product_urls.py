from django.urls import path
from groceryplusv1.views import product_views

urlpatterns = [
    path(
        "products/get-products",
        product_views.get_products,
        name="get_products",
    ),
    path(
        "products/create-product", product_views.create_product, name="create_product"
    ),
    path(
        "products/update-product/<str:id>",
        product_views.update_product,
        name="update_product",
    ),
    path(
        "products/delete-product/<str:id>",
        product_views.delete_product,
        name="delete_product",
    ),
    path(
        "products/delete-all-product",
        product_views.delete_all_product,
        name="delete_all_product",
    ),
]
