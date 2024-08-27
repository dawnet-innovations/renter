from django.urls import path, include

urlpatterns = [
    path("", include("users.general.urls")),
    path("password/forgot/", include("users.reset_password.urls")),
    path("password/change/", include("users.change_password.urls")),
]
