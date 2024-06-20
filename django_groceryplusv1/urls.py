from django.urls import path, include

urlpatterns = [
    path("groceryplus/", include("groceryplusv1.urls.user_urls")),
    path("groceryplus/", include("groceryplusv1.urls.product_urls")),
]
