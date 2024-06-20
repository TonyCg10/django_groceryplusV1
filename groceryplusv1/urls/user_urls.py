from django.urls import path
from groceryplusv1.views import user_views

urlpatterns = [
    path("users/get-users", user_views.get_users, name="get_users"),
    path("users/create-user", user_views.create_user, name="create_user"),
    path("users/check-user", user_views.check_user, name="check_user"),
    path(
        "users/update-user/<str:id>",
        user_views.update_user,
        name="update_user",
    ),
    path(
        "users/delete-user/<str:id>",
        user_views.delete_user,
        name="delete_user",
    ),
]
